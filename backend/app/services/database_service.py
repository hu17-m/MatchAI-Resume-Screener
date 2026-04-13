from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging
import os

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self.collection = None

    async def connect(self) -> bool:
        try:
            mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
            self.client = AsyncIOMotorClient(mongo_uri)
            self.db = self.client.resume_ai_db
            self.collection = self.db.resume_analyses

            await self.client.admin.command('ping')
            logger.info("✅ MongoDB Connected")

            await self._create_indexes()
            return True
        except Exception as e:
            logger.warning(f"❌ MongoDB connection failed: {e}")
            return False

    async def _create_indexes(self):
        try:
            await self.collection.create_index("id", unique=True)
            await self.collection.create_index("userId")
            await self.collection.create_index("createdAt")
        except Exception as e:
            logger.warning(f"Index warning: {e}")

    def is_connected(self) -> bool:
        return self.collection is not None

    def _serialize(self, data):
        """Recursively convert ObjectId and Datetime to JSON-serializable formats."""
        if data is None:
            return None
        if isinstance(data, ObjectId):
            return str(data)
        if isinstance(data, datetime):
            return data.isoformat()
        if isinstance(data, list):
            return [self._serialize(item) for item in data]
        if isinstance(data, dict):
            return {k: self._serialize(v) for k, v in data.items()}
        return data

    async def save_analysis(self, analysis_data: Dict[str, Any]) -> Optional[str]:
        if not self.is_connected():
            return None
        try:
            document = {
                **analysis_data,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }
            result = await self.collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Save error: {e}")
            return None

    async def get_analysis_by_id(self, analysis_id: str, user_id: str):
        """Fetch a single analysis ONLY if it belongs to the requesting user."""
        if not self.is_connected() or not user_id:
            return None
        try:
            # Query strictly by both ID and userId for privacy
            query = {"id": analysis_id, "userId": user_id}
            document = await self.collection.find_one(query)

            # Fallback to _id if standard id fails
            if not document:
                try:
                    document = await self.collection.find_one({"_id": ObjectId(analysis_id), "userId": user_id})
                except:
                    pass

            return self._serialize(document) if document else None
        except Exception as e:
            logger.error(f"Get single error: {e}")
            return None

    async def get_all_analyses(self, limit=50, skip=0, user_id=None) -> List[Dict]:
        """Fetch history ONLY for the logged-in user."""
        if not self.is_connected() or not user_id:
            return []
        try:
            query = {"userId": user_id}
            cursor = self.collection.find(query)\
                .sort("createdAt", -1)\
                .skip(skip)\
                .limit(limit)

            results = []
            async for doc in cursor:
                results.append(self._serialize(doc))
            return results
        except Exception as e:
            logger.error(f"Get all error: {e}")
            return []

    async def delete_analysis(self, analysis_id: str, user_id: str) -> bool:
        if not self.is_connected() or not user_id:
            return False
        try:
            # Only delete if user owns the record
            result = await self.collection.delete_one({"id": analysis_id, "userId": user_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Delete error: {e}")
            return False

    async def get_analytics(self, user_id=None):
        """Aggregate data ONLY for the specific user."""
        if not self.is_connected() or not user_id:
            return self._empty()
        try:
            pipeline = [
                {"$match": {"userId": user_id}},  # ✅ Privacy Filter
                {
                    "$group": {
                        "_id": None,
                        "totalAnalyses": {"$sum": 1},
                        "averageScore": {"$avg": "$overallScore"},
                        "averageAtsScore": {"$avg": "$atsScore"}
                    }
                }
            ]
            result = await self.collection.aggregate(pipeline).to_list(1)
            if result:
                r = result[0]
                return {
                    "totalAnalyses": r.get("totalAnalyses", 0),
                    "averageScore": round(r.get("averageScore", 0) or 0, 1),
                    "averageAtsScore": round(r.get("averageAtsScore", 0) or 0, 1),
                    "categoryDistribution": {},
                    "topSkills": []
                }
            return self._empty()
        except Exception as e:
            logger.error(f"Analytics error: {e}")
            return self._empty()

    def _empty(self):
        return {
            "totalAnalyses": 0, "averageScore": 0, "averageAtsScore": 0,
            "categoryDistribution": {}, "topSkills": []
        }

    async def disconnect(self):
        if self.client:
            self.client.close()

db_service = DatabaseService()
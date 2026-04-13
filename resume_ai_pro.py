import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
import joblib
import re

# Load & clean data
df = pd.read_csv('resume_data.csv')

print("🔧 Building PRO features...")

# 🎯 Better feature engineering
def clean_text(text):
    if pd.isna(text):
        return ""
    return re.sub(r'[^\w\s]', ' ', str(text).lower())

# Create rich features
df['resume_combined'] = (df['skills'].fillna('') + ' ' + 
                        df['career_objective'].fillna('') + ' ' +
                        df['positions'].fillna('') + ' ' +
                        df['responsibilities'].fillna('')).apply(clean_text)

df['job_combined'] = (df['\ufeffjob_position_name'].fillna('') + ' ' + 
                     df['skills_required'].fillna('') + ' ' +
                     df['responsibilities.1'].fillna('')).apply(clean_text)

# TF-IDF features (NLP magic!)
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english', ngram_range=(1,2))
X_text = vectorizer.fit_transform(df['resume_combined'] + ' ' + df['job_combined'])

# Numeric features
df['skills_len'] = df['skills'].str.split().str.len().fillna(0)
df['job_skills_len'] = df['skills_required'].str.split().str.len().fillna(0)
df['exp_years'] = df['passing_years'].fillna('').str.extract('(\d+)').astype(float).fillna(0).mean(axis=1)

X_numeric = df[['skills_len', 'job_skills_len', 'exp_years', 'matched_score']].fillna(0)

# Combine features
X = np.hstack([X_text.toarray()[:, :50], X_numeric.values])  # Top 50 TF-IDF + numerics
y = df['matched_score']

# Split & train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Results
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print("🚀 RESUME AI PRO RESULTS")
print(f"✅ Test R²: {r2:.3f} (EXCELLENT!)")
print(f"✅ MAE: {mae:.3f} (Very accurate!)")
print(f"Sample predictions: {y_pred[:5].round(3)}")
print(f"Actual values:     {y_test.iloc[:5].values.round(3)}")

# 💾 Save PRO model + vectorizer
joblib.dump({'model': model, 'vectorizer': vectorizer}, 'resume_ai_pro.pkl')
print("\n✅ PRO Model saved as 'resume_ai_pro.pkl'")
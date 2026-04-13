import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('resume_data.csv')

print("📊 DATASET OVERVIEW")
print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"Match scores: {df['matched_score'].min():.3f} - {df['matched_score'].max():.3f}")
print(f"Average score: {df['matched_score'].mean():.3f}")

print("\n🔥 TOP 10 MOST COMMON SKILLS")
if 'skills' in df.columns:
    top_skills = df['skills'].dropna().str.split(',|;').explode().str.strip().value_counts()
    print(top_skills.head(10))

print("\n💼 TOP 10 JOB POSITIONS")
job_col = '\ufeffjob_position_name'
if job_col in df.columns:
    print(df[job_col].value_counts().head(10))

print("\n📈 MATCH SCORE ANALYSIS")
plt.style.use('default')
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Histogram
axes[0].hist(df['matched_score'], bins=30, edgecolor='black', alpha=0.7)
axes[0].set_title('Match Score Distribution')
axes[0].set_xlabel('Match Score')
axes[0].set_ylabel('Frequency')

# Boxplot
sns.boxplot(y=df['matched_score'], ax=axes[1])
axes[1].set_title('Match Score Boxplot')

plt.tight_layout()
plt.savefig('match_score_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Charts saved as 'match_score_analysis.png'")
print("\n🎯 NEXT STEPS READY!")
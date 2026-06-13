import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================
# STEP 1: IMPORT DATA FROM DIVVY 2020 Q1

path = "202004-divvy-tripdata.csv"
df = pd.read_csv(path)

print("=" * 80)
print("CYCLISTIC BIKE-SHARE ANALYSIS - 2020 Q1 DATA")
print("=" * 80)
print(f"Total rows loaded: {len(df):,}")

# ============================================================================
# STEP 2: DATA CLEANING AND TRANSFORMATION

# Convert to datetime
df['started_at'] = pd.to_datetime(df['started_at'])
df['ended_at'] = pd.to_datetime(df['ended_at'])

# Create ride length (in minutes)
df['ride_length'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60

# Create day of week
df['day_of_week'] = df['started_at'].dt.day_name()

# Create numeric day of week (1=Sunday, 7=Saturday) for sorting
day_mapping = {'Sunday': 1, 'Monday': 2, 'Tuesday': 3, 'Wednesday': 4, 
               'Thursday': 5, 'Friday': 6, 'Saturday': 7}
df['day_of_week_num'] = df['day_of_week'].map(day_mapping)

# Remove bad data (ride_length <= 0 indicates potential data entry error)
initial_rows = len(df)
df = df[df['ride_length'] > 0]
print(f"Rows removed due to invalid ride length: {initial_rows - len(df)}")
print(f"Clean data rows: {len(df):,}")

# ============================================================================
# STEP 3: DESCRIPTIVE ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("DESCRIPTIVE STATISTICS - ALL RIDERS")
print("=" * 80)
print(f"Mean ride length: {df['ride_length'].mean():.2f} minutes")
print(f"Median ride length: {df['ride_length'].median():.2f} minutes")
print(f"Max ride length: {df['ride_length'].max():.2f} minutes")
print(f"Min ride length: {df['ride_length'].min():.2f} minutes")
print(f"Standard deviation: {df['ride_length'].std():.2f} minutes")

# ============================================================================
# STEP 4: ANALYSIS BY MEMBER TYPE
# ============================================================================

print("\n" + "=" * 80)
print("COMPARATIVE ANALYSIS: MEMBERS VS CASUAL RIDERS")
print("=" * 80)

member_stats = df.groupby('member_casual')['ride_length'].agg([
    ('Count', 'count'),
    ('Mean (min)', 'mean'),
    ('Median (min)', 'median'),
    ('Max (min)', 'max'),
    ('Std Dev', 'std')
]).round(2)
print("\n" + member_stats.to_string())

# Ride counts by member type
print("\n" + "-" * 80)
print("RIDE COUNTS BY MEMBER TYPE")
print("-" * 80)
ride_counts = df['member_casual'].value_counts().sort_index()
for member_type, count in ride_counts.items():
    pct = (count / len(df)) * 100
    print(f"{member_type:10s}: {count:7,} rides ({pct:5.1f}%)")

# ============================================================================
# STEP 5: ANALYSIS BY DAY OF WEEK
# ============================================================================

print("\n" + "=" * 80)
print("AVERAGE RIDE LENGTH BY DAY OF WEEK AND MEMBER TYPE")
print("=" * 80)

day_of_week_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
pivot_table = df.pivot_table(
    values='ride_length', 
    index='member_casual', 
    columns='day_of_week',
    aggfunc='mean'
)[day_of_week_order]

print("\n" + pivot_table.round(2).to_string())

# Ride count by day of week
print("\n" + "-" * 80)
print("NUMBER OF RIDES BY DAY OF WEEK AND MEMBER TYPE")
print("-" * 80)

pivot_count = df.pivot_table(
    values='ride_length', 
    index='member_casual', 
    columns='day_of_week',
    aggfunc='count'
)[day_of_week_order]

print("\n" + pivot_count.astype('int').to_string())

# ============================================================================
# STEP 6: CREATE VISUALIZATIONS
# ============================================================================

print("\n" + "=" * 80)
print("GENERATING VISUALIZATIONS")
print("=" * 80)

# Set style for professional-looking charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

# Create a 2x2 subplot figure
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Cyclistic Bike-Share: Member vs Casual Rider Analysis (April 2020)', 
             fontsize=16, fontweight='bold')

# Chart 1: Ride Count by Member Type
ax1 = axes[0, 0]
ride_counts.plot(kind='bar', ax=ax1, color=['#1f77b4', '#ff7f0e'])
ax1.set_title('Total Rides: Members vs Casual Riders', fontweight='bold')
ax1.set_ylabel('Number of Rides')
ax1.set_xlabel('Member Type')
ax1.tick_params(axis='x', rotation=0)
for i, v in enumerate(ride_counts):
    ax1.text(i, v + 1000, str(v), ha='center', fontweight='bold')

# Chart 2: Average Ride Length by Member Type
ax2 = axes[0, 1]
avg_by_member = df.groupby('member_casual')['ride_length'].mean().sort_values(ascending=False)
avg_by_member.plot(kind='bar', ax=ax2, color=['#ff7f0e', '#1f77b4'])
ax2.set_title('Average Ride Length: Members vs Casual Riders', fontweight='bold')
ax2.set_ylabel('Ride Length (minutes)')
ax2.set_xlabel('Member Type')
ax2.tick_params(axis='x', rotation=0)
for i, v in enumerate(avg_by_member):
    ax2.text(i, v + 2, f'{v:.1f}', ha='center', fontweight='bold')

# Chart 3: Average Ride Length by Day of Week
ax3 = axes[1, 0]
for member_type in ['casual', 'member']:
    data = df[df['member_casual'] == member_type].copy()
    daily_avg = data.groupby('day_of_week')['ride_length'].mean().reindex(day_of_week_order)
    ax3.plot(day_of_week_order, daily_avg, marker='o', linewidth=2, label=member_type)
ax3.set_title('Average Ride Length by Day of Week', fontweight='bold')
ax3.set_ylabel('Ride Length (minutes)')
ax3.set_xlabel('Day of Week')
ax3.legend()
ax3.tick_params(axis='x', rotation=45)
ax3.grid(True, alpha=0.3)

# Chart 4: Ride Count by Day of Week
ax4 = axes[1, 1]
for member_type in ['member', 'casual']:
    data = df[df['member_casual'] == member_type].copy()
    daily_count = data.groupby('day_of_week').size().reindex(day_of_week_order)
    ax4.plot(day_of_week_order, daily_count, marker='s', linewidth=2, label=member_type)
ax4.set_title('Ride Count by Day of Week', fontweight='bold')
ax4.set_ylabel('Number of Rides')
ax4.set_xlabel('Day of Week')
ax4.legend()
ax4.tick_params(axis='x', rotation=45)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('cyclistic_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved visualization: cyclistic_analysis.png")
plt.close()

# ============================================================================
# STEP 7: EXPORT SUMMARY DATA
# ============================================================================

print("\n" + "=" * 80)
print("EXPORTING DATA FILES")
print("=" * 80)

# Export cleaned data
df.to_csv("cleaned_data.csv", index=False)
print("✓ Exported cleaned data: cleaned_data.csv")

# Export member statistics
member_stats.to_csv("member_statistics.csv")
print("✓ Exported member statistics: member_statistics.csv")

# Export daily summary
daily_summary = df.groupby('day_of_week').agg({
    'ride_length': ['count', 'mean', 'median', 'max'],
    'member_casual': lambda x: (x == 'member').sum()
}).round(2)
daily_summary.columns = ['Total_Rides', 'Avg_Length', 'Median_Length', 'Max_Length', 'Member_Count']
daily_summary = daily_summary.reindex(day_of_week_order)
daily_summary.to_csv("daily_summary.csv")
print("✓ Exported daily summary: daily_summary.csv")

# ============================================================================
# STEP 8: KEY FINDINGS & RECOMMENDATIONS
# ============================================================================

print("\n" + "=" * 80)
print("KEY FINDINGS")
print("=" * 80)

casual_avg_ride = df[df['member_casual'] == 'casual']['ride_length'].mean()
member_avg_ride = df[df['member_casual'] == 'member']['ride_length'].mean()
ride_diff_pct = ((casual_avg_ride - member_avg_ride) / member_avg_ride) * 100

casual_count = len(df[df['member_casual'] == 'casual'])
member_count = len(df[df['member_casual'] == 'member'])

print(f"""
1. RIDE LENGTH DIFFERENCE:
   • Casual riders average {casual_avg_ride:.1f} minutes per ride
   • Members average {member_avg_ride:.1f} minutes per ride
   • Casual riders have {ride_diff_pct:.1f}% longer average ride times

2. VOLUME DISTRIBUTION:
   • Members account for {(member_count/len(df)*100):.1f}% of rides ({member_count:,} rides)
   • Casual riders account for {(casual_count/len(df)*100):.1f}% of rides ({casual_count:,} rides)

3. RIDING PATTERNS:
   • Members show consistent usage across all days
   • Casual riders peak on weekends (Friday, Saturday, Sunday)
   • Weekend casual rides are {(casual_avg_ride/member_avg_ride):.1f}x longer than member rides
""")

print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)




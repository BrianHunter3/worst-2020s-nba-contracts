import pandas as pd
import matplotlib.pyplot as plt

# -- DataFrame Loading...
df = pd.read_csv(r'C:\Users\hoode\Downloads\worst-2020s-nba-contracts\nba_contracts.csv', skiprows=4)
df = df.dropna(how='all', axis=1) # Drops the 2 empty columns on the left
pd.set_option('display.width', 1500) # Widening terminal display

# -- Data Cleaning... --
df.columns = df.columns.str.lower().str.replace('%', '_pct')
df = df.dropna(subset=['annual_salary']) # Drops rows with no salary data
df['player'] = df['player'].replace('D?vis Bert?ns', 'Davis Bertans')
# Converts blank stats to 0
for col in ['gp', 'min', 'pie']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
# Cleaning salary and inserting 'salary_millions' to the left of 'annual_salary'
salary_m = (
    df['annual_salary']
    .str.replace('$', '', regex=False) # regex=False tells Pandas to treat $ as a literal dollar sign
    .str.replace(',', '', regex=False)
    .astype(float) / 1_000_000
)
salary_index = df.columns.get_loc('annual_salary')
df.insert(loc=salary_index, column='salary_millions', value=salary_m) # Modifies df in-place rather than appending to end as standard
# Inserting 'mpg' to the right of 'min'
min_index = df.columns.get_loc('min')
df.insert(loc=min_index + 1, column='mpg', value=(df['min'] / df['gp']).fillna(0))

# -- Mathing... --
# Calculating ROI
df['pie_dec'] = df['pie'] / 100
gross_roi = ((df['gp'] * df['mpg'] * df['pie_dec']) / df['salary_millions']).fillna(0)
df['roi'] = ((gross_roi - 10) / 10) * 100

print('Tier 1: Toxic Assets / Dead Money    (Net ROI < -75%)   -> Complete disaster / Buyouts (-100%)')
print('Tier 2: Inefficient Contracts        (-75% to -40%)     -> Heavy overpay for starter production')
print('Tier 3: Below-Average Value          (-40% to -10%)     -> Modest overpay / durability issues')
print('Tier 4: Fair Market Value            (-10% to +15%)     -> Expected production for the paycheck')
print('Tier 5: Surplus Value                (> +15%)           -> Underpaid / high bargain value')

# Creating a tier column to conveniently read
tier_bins = [-float('inf'), -75, -40, -10, 15, float('inf')]
tier_labels = ['Tier 1: Toxic', 'Tier 2: Inefficient', 'Tier 3: Below-Average', 'Tier 4: Fair Value', 'Tier 5: Surplus']
df['tier'] = pd.cut(df['roi'], bins=tier_bins, labels=tier_labels)
df['wasted_salary_m'] = (df['salary_millions'] * (-df['roi'] / 100)).round(2)

cols_to_view = ['player', 'season', 'team', 'salary_millions', 'wasted_salary_m', 'gp', 'pie', 'roi', 'tier']
print(f'\n', df[cols_to_view].sort_values(
    by=['roi', 'salary_millions'], 
    ascending=[True, False]
))

# ==========================================
# VISUALIZATION
# ==========================================

# Chart 1: Top 10 Most Toxic Contract Seasons
plt.figure(figsize=(11, 6))

top_10_worst = df.sort_values(
    by=['roi', 'salary_millions'], 
    ascending=[True, False]
).head(10).copy()

# Bar labels
bar_labels = (
    top_10_worst['player'] 
    + " (" + top_10_worst['season'] + ", " + top_10_worst['team'] + ") - $" 
    + top_10_worst['salary_millions'].round(1).astype(str) + "M"
)

# Plot horizontal bars
bars = plt.barh(bar_labels, top_10_worst['roi'], color='#C9082A', edgecolor='black')

plt.title('Top 10 Worst NBA Contract Seasons (2020s)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Net ROI (%)  [0% = Fair Market Value Break-Even]', fontsize=11)
plt.axvline(0, color='black', linestyle='--', linewidth=1, label='Fair Market Value (0%)')
plt.xlim(-110, 5)

plt.gca().invert_yaxis() # Inverting so Beal's #1

# Add value labels directly on the bars (e.g., "-100.0%")
for bar in bars:
    width = bar.get_width()
    plt.text(width - 1, bar.get_y() + bar.get_height()/2, f"{width:.1f}%", 
             va='center', ha='right', color='white', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.show()

# Chart 2: Salary vs. Net ROI Scatter Plot Contract Matrix
plt.figure(figsize=(11, 7))

# Distinct color palette for each tier
tier_colors = {
    'Tier 1: Toxic': '#C9082A',
    'Tier 2: Inefficient': '#ff7f0e',
    'Tier 3: Below-Average': '#17408B',
    'Tier 4: Fair Value': '#2ca02c',
}

for tier_name, color in tier_colors.items():
    tier_data = df[df['tier'] == tier_name]
    plt.scatter(
        tier_data['salary_millions'], 
        tier_data['roi'], 
        label=tier_name, 
        color=color, 
        alpha=0.75, 
        s=85, 
        edgecolor='black'
    )

# Baseline reference line
plt.axhline(0, color='black', linestyle='--', linewidth=1.2, label='Break-Even (0% Net ROI)')

plt.title('NBA Contracts: Annual Salary ($M) vs. Net ROI (%)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Annual Salary ($ Millions)', fontsize=11)
plt.ylabel('Net ROI (%)', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.5)

labeled_points = df[df['tier'].isin(['Tier 1: Toxic', 'Tier 4: Fair Value'])]
for _, row in labeled_points.iterrows():
    # Subtle badge color: soft red for toxic, soft green for fair value
    badge_color = '#ffcdd2' if row['tier'] == 'Tier 1: Toxic' else '#c8e6c9'
    
    plt.annotate(
        f"{row['player']} ('{row['season'][-2:]})",
        (row['salary_millions'], row['roi']),
        textcoords="offset points",
        xytext=(8, 4),
        fontweight='bold',
        fontsize=8,
        bbox=dict(boxstyle="round,pad=0.2", facecolor=badge_color, alpha=0.6, edgecolor="gray")
    )
# 2. Move the legend outside to the right of the graph
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
plt.tight_layout()
plt.show()
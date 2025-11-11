# ============================================================================
# VISUALIZATION SCRIPT FOR SPARK STREAMING LAB RESULTS
# ============================================================================
# This script creates comprehensive visualizations from the stock streaming data
# Run: python visualize_results.py

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
import numpy as np

# Set style
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    try:
        plt.style.use('seaborn-darkgrid')
    except:
        plt.style.use('ggplot')
sns.set_palette("husl")

# Get script directory
SCRIPT_DIR = Path(__file__).parent.absolute()
STOCK_STREAM_DIR = SCRIPT_DIR / "stock_stream"

print("="*70)
print("SPARK STREAMING LAB - DATA VISUALIZATION")
print("="*70)
print()

# Load all batch files
print("Loading data from batch files...")
all_data = []

batch_files = sorted(STOCK_STREAM_DIR.glob("batch_*.json"))
print(f"Found {len(batch_files)} batch files")

for batch_file in batch_files:
    try:
        with open(batch_file, 'r') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    # Skip INIT records
                    if data.get('symbol') != 'INIT':
                        all_data.append(data)
    except Exception as e:
        print(f"Warning: Could not read {batch_file}: {e}")

if not all_data:
    print("ERROR: No data found. Please run lab7.py first to generate data.")
    exit(1)

# Convert to DataFrame
df = pd.DataFrame(all_data)
df['timestamp'] = pd.to_datetime(df['timestamp'])

print(f"[OK] Loaded {len(df)} records")
print(f"[OK] Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"[OK] Symbols: {', '.join(df['symbol'].unique())}")
print()

# Calculate additional metrics
df = df.sort_values('timestamp')
df['price_change'] = df.groupby('symbol')['price'].diff()
df['price_change_pct'] = df.groupby('symbol')['price'].pct_change() * 100
df['volatility'] = df.groupby('symbol')['price_change_pct'].rolling(window=5, min_periods=1).std().reset_index(0, drop=True)

# Create output directory for plots
output_dir = SCRIPT_DIR / "visualizations"
output_dir.mkdir(exist_ok=True)

print("Creating visualizations...")
print()

# ============================================================================
# 1. PRICE TRENDS OVER TIME
# ============================================================================
print("1. Price Trends Over Time...")
fig, ax = plt.subplots(figsize=(14, 8))
for symbol in df['symbol'].unique():
    symbol_data = df[df['symbol'] == symbol]
    ax.plot(symbol_data['timestamp'], symbol_data['price'], 
            label=symbol, linewidth=2, marker='o', markersize=3, alpha=0.7)

ax.set_xlabel('Time', fontsize=12, fontweight='bold')
ax.set_ylabel('Price ($)', fontsize=12, fontweight='bold')
ax.set_title('Stock Price Trends Over Time', fontsize=14, fontweight='bold')
ax.legend(loc='best', frameon=True, shadow=True)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_dir / '1_price_trends.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir / '1_price_trends.png'}")
plt.close()

# ============================================================================
# 2. PRICE DISTRIBUTION BY STOCK
# ============================================================================
print("2. Price Distribution by Stock...")
fig, ax = plt.subplots(figsize=(12, 6))
df.boxplot(column='price', by='symbol', ax=ax, grid=False)
ax.set_xlabel('Stock Symbol', fontsize=12, fontweight='bold')
ax.set_ylabel('Price ($)', fontsize=12, fontweight='bold')
ax.set_title('Price Distribution by Stock', fontsize=14, fontweight='bold')
plt.suptitle('')  # Remove default title
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_dir / '2_price_distribution.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir / '2_price_distribution.png'}")
plt.close()

# ============================================================================
# 3. VOLATILITY ANALYSIS
# ============================================================================
print("3. Volatility Analysis...")
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Volatility over time
for symbol in df['symbol'].unique():
    symbol_data = df[df['symbol'] == symbol]
    axes[0].plot(symbol_data['timestamp'], symbol_data['volatility'], 
                 label=symbol, linewidth=2, alpha=0.7)

axes[0].set_xlabel('Time', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Volatility (%)', fontsize=12, fontweight='bold')
axes[0].set_title('Volatility Over Time', fontsize=14, fontweight='bold')
axes[0].legend(loc='best', frameon=True, shadow=True)
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# Average volatility by stock
avg_volatility = df.groupby('symbol')['volatility'].mean().sort_values(ascending=False)
axes[1].bar(avg_volatility.index, avg_volatility.values, color=sns.color_palette("husl", len(avg_volatility)))
axes[1].set_xlabel('Stock Symbol', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Average Volatility (%)', fontsize=12, fontweight='bold')
axes[1].set_title('Average Volatility by Stock', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(output_dir / '3_volatility_analysis.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir / '3_volatility_analysis.png'}")
plt.close()

# ============================================================================
# 4. VOLUME ANALYSIS
# ============================================================================
print("4. Volume Analysis...")
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Volume over time
for symbol in df['symbol'].unique():
    symbol_data = df[df['symbol'] == symbol]
    axes[0].plot(symbol_data['timestamp'], symbol_data['volume'], 
                 label=symbol, linewidth=2, alpha=0.7, marker='o', markersize=2)

axes[0].set_xlabel('Time', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Volume', fontsize=12, fontweight='bold')
axes[0].set_title('Trading Volume Over Time', fontsize=14, fontweight='bold')
axes[0].legend(loc='best', frameon=True, shadow=True)
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# Total volume by stock
total_volume = df.groupby('symbol')['volume'].sum().sort_values(ascending=False)
axes[1].bar(total_volume.index, total_volume.values, color=sns.color_palette("husl", len(total_volume)))
axes[1].set_xlabel('Stock Symbol', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Total Volume', fontsize=12, fontweight='bold')
axes[1].set_title('Total Trading Volume by Stock', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(output_dir / '4_volume_analysis.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir / '4_volume_analysis.png'}")
plt.close()

# ============================================================================
# 5. PRICE CHANGE ANALYSIS
# ============================================================================
print("5. Price Change Analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Price change distribution
df['price_change'].hist(bins=50, ax=axes[0, 0], edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Price Change ($)', fontsize=11, fontweight='bold')
axes[0, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
axes[0, 0].set_title('Price Change Distribution', fontsize=12, fontweight='bold')
axes[0, 0].axvline(x=0, color='red', linestyle='--', linewidth=2)
axes[0, 0].grid(True, alpha=0.3)

# Price change by symbol
df.boxplot(column='price_change', by='symbol', ax=axes[0, 1], grid=False)
axes[0, 1].set_xlabel('Stock Symbol', fontsize=11, fontweight='bold')
axes[0, 1].set_ylabel('Price Change ($)', fontsize=11, fontweight='bold')
axes[0, 1].set_title('Price Change by Stock', fontsize=12, fontweight='bold')
plt.suptitle('')
axes[0, 1].axhline(y=0, color='red', linestyle='--', linewidth=2)

# Percentage change distribution
df['price_change_pct'].hist(bins=50, ax=axes[1, 0], edgecolor='black', alpha=0.7)
axes[1, 0].set_xlabel('Price Change (%)', fontsize=11, fontweight='bold')
axes[1, 0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
axes[1, 0].set_title('Percentage Change Distribution', fontsize=12, fontweight='bold')
axes[1, 0].axvline(x=0, color='red', linestyle='--', linewidth=2)
axes[1, 0].grid(True, alpha=0.3)

# Average price change by symbol
avg_change = df.groupby('symbol')['price_change_pct'].mean().sort_values(ascending=False)
axes[1, 1].bar(avg_change.index, avg_change.values, color=sns.color_palette("husl", len(avg_change)))
axes[1, 1].set_xlabel('Stock Symbol', fontsize=11, fontweight='bold')
axes[1, 1].set_ylabel('Average Price Change (%)', fontsize=11, fontweight='bold')
axes[1, 1].set_title('Average Percentage Change by Stock', fontsize=12, fontweight='bold')
axes[1, 1].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(output_dir / '5_price_change_analysis.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir / '5_price_change_analysis.png'}")
plt.close()

# ============================================================================
# 6. CORRELATION HEATMAP
# ============================================================================
print("6. Correlation Analysis...")
# Pivot price data for correlation
price_pivot = df.pivot_table(index='timestamp', columns='symbol', values='price', aggfunc='mean')
correlation_matrix = price_pivot.corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
ax.set_title('Stock Price Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(output_dir / '6_correlation_heatmap.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir / '6_correlation_heatmap.png'}")
plt.close()

# ============================================================================
# 7. VALUE AT RISK (VaR) VISUALIZATION
# ============================================================================
print("7. Value at Risk (VaR) Analysis...")
# Calculate VaR for each stock (95% confidence level)
var_data = []
for symbol in df['symbol'].unique():
    symbol_data = df[df['symbol'] == symbol]
    avg_price = symbol_data['price'].mean()
    volatility = symbol_data['volatility'].mean()
    # VaR at 95% confidence (1.645 standard deviations)
    var_95 = 1.645 * volatility * avg_price / 100  # Convert volatility % to absolute
    
    var_data.append({
        'symbol': symbol,
        'avg_price': avg_price,
        'volatility': volatility,
        'VaR_95': var_95,
        'VaR_pct': 1.645 * volatility
    })

var_df = pd.DataFrame(var_data).sort_values('VaR_95', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# VaR in absolute terms
axes[0].bar(var_df['symbol'], var_df['VaR_95'], color=sns.color_palette("husl", len(var_df)))
axes[0].set_xlabel('Stock Symbol', fontsize=12, fontweight='bold')
axes[0].set_ylabel('VaR at 95% Confidence ($)', fontsize=12, fontweight='bold')
axes[0].set_title('Value at Risk (95% Confidence) - Absolute', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='y')
for i, v in enumerate(var_df['VaR_95']):
    axes[0].text(i, v, f'${v:.2f}', ha='center', va='bottom', fontweight='bold')

# VaR as percentage
axes[1].bar(var_df['symbol'], var_df['VaR_pct'], color=sns.color_palette("husl", len(var_df)))
axes[1].set_xlabel('Stock Symbol', fontsize=12, fontweight='bold')
axes[1].set_ylabel('VaR at 95% Confidence (%)', fontsize=12, fontweight='bold')
axes[1].set_title('Value at Risk (95% Confidence) - Percentage', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')
for i, v in enumerate(var_df['VaR_pct']):
    axes[1].text(i, v, f'{v:.2f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '7_var_analysis.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir / '7_var_analysis.png'}")
plt.close()

# ============================================================================
# 8. COMPREHENSIVE DASHBOARD
# ============================================================================
print("8. Creating Comprehensive Dashboard...")
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 1. Price trends (top left, spans 2 columns)
ax1 = fig.add_subplot(gs[0, :2])
for symbol in df['symbol'].unique():
    symbol_data = df[df['symbol'] == symbol]
    ax1.plot(symbol_data['timestamp'], symbol_data['price'], label=symbol, linewidth=2, alpha=0.7)
ax1.set_title('Price Trends', fontsize=12, fontweight='bold')
ax1.set_xlabel('Time')
ax1.set_ylabel('Price ($)')
ax1.legend(loc='best', fontsize=8)
ax1.grid(True, alpha=0.3)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

# 2. Volatility comparison (top right)
ax2 = fig.add_subplot(gs[0, 2])
avg_volatility = df.groupby('symbol')['volatility'].mean().sort_values(ascending=False)
ax2.barh(avg_volatility.index, avg_volatility.values, color=sns.color_palette("husl", len(avg_volatility)))
ax2.set_title('Avg Volatility', fontsize=12, fontweight='bold')
ax2.set_xlabel('Volatility (%)')
ax2.grid(True, alpha=0.3, axis='x')

# 3. Volume comparison (middle left)
ax3 = fig.add_subplot(gs[1, 0])
total_volume = df.groupby('symbol')['volume'].sum().sort_values(ascending=False)
ax3.bar(total_volume.index, total_volume.values, color=sns.color_palette("husl", len(total_volume)))
ax3.set_title('Total Volume', fontsize=12, fontweight='bold')
ax3.set_ylabel('Volume')
ax3.grid(True, alpha=0.3, axis='y')

# 4. Price distribution (middle center)
ax4 = fig.add_subplot(gs[1, 1])
df.boxplot(column='price', by='symbol', ax=ax4, grid=False)
ax4.set_title('Price Distribution', fontsize=12, fontweight='bold')
ax4.set_xlabel('Symbol')
ax4.set_ylabel('Price ($)')
plt.suptitle('')

# 5. VaR (middle right)
ax5 = fig.add_subplot(gs[1, 2])
ax5.bar(var_df['symbol'], var_df['VaR_95'], color=sns.color_palette("husl", len(var_df)))
ax5.set_title('Value at Risk (95%)', fontsize=12, fontweight='bold')
ax5.set_ylabel('VaR ($)')
ax5.grid(True, alpha=0.3, axis='y')
plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45)

# 6. Correlation heatmap (bottom, spans 3 columns)
ax6 = fig.add_subplot(gs[2, :])
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax6)
ax6.set_title('Price Correlation Matrix', fontsize=12, fontweight='bold')

fig.suptitle('Spark Streaming Lab - Comprehensive Dashboard', fontsize=16, fontweight='bold', y=0.995)
plt.savefig(output_dir / '8_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
print(f"   [OK] Saved: {output_dir / '8_comprehensive_dashboard.png'}")
plt.close()

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
print()
print("="*70)
print("SUMMARY STATISTICS")
print("="*70)
print()
summary = df.groupby('symbol').agg({
    'price': ['mean', 'std', 'min', 'max'],
    'volume': ['sum', 'mean'],
    'volatility': 'mean',
    'price_change_pct': 'mean'
}).round(2)
print(summary)
print()

# Save summary to CSV
summary.to_csv(output_dir / 'summary_statistics.csv')
print(f"[OK] Summary statistics saved to: {output_dir / 'summary_statistics.csv'}")
print()

print("="*70)
print("[SUCCESS] VISUALIZATION COMPLETE!")
print("="*70)
print(f"All visualizations saved to: {output_dir}")
print()
print("Generated files:")
for i, file in enumerate(sorted(output_dir.glob("*.png")), 1):
    print(f"  {i}. {file.name}")


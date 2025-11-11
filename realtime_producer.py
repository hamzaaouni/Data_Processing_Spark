# ============================================================================
# REAL-TIME STOCK DATA PRODUCER FOR DASHBOARD
# ============================================================================
# This script continuously generates new stock data every 10 seconds
# Run: python realtime_producer.py
# Keep this running while using the dashboard for real-time updates

import json
import random
import time
import os
from datetime import datetime
from pathlib import Path

# Get script directory
SCRIPT_DIR = Path(__file__).parent.absolute()
STOCK_STREAM_DIR = SCRIPT_DIR / "stock_stream"
STOCK_STREAM_DIR.mkdir(parents=True, exist_ok=True)

class RealTimeStockProducer:
    def __init__(self, output_path=None):
        if output_path is None:
            output_path = str(STOCK_STREAM_DIR)
        self.output_path = output_path
        self.symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
        
        # Initialize prices (can load from last batch or use defaults)
        self.prices = self._load_last_prices() or {
            'AAPL': 180.0, 
            'GOOGL': 140.0, 
            'MSFT': 370.0, 
            'AMZN': 145.0, 
            'TSLA': 240.0
        }
        
        self.running = False
        self.batch_num = self._get_next_batch_num()
        
    def _get_next_batch_num(self):
        """Get the next batch number from existing files"""
        batch_files = list(STOCK_STREAM_DIR.glob("batch_*.json"))
        if batch_files:
            # Extract numbers and find max
            numbers = []
            for f in batch_files:
                try:
                    num = int(f.stem.split('_')[1])
                    numbers.append(num)
                except:
                    pass
            return max(numbers) + 1 if numbers else 0
        return 0
    
    def _load_last_prices(self):
        """Load last known prices from the most recent batch file"""
        batch_files = sorted(STOCK_STREAM_DIR.glob("batch_*.json"))
        if not batch_files:
            return None
        
        # Get the most recent batch
        last_batch = batch_files[-1]
        prices = {}
        
        try:
            with open(last_batch, 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        symbol = data.get('symbol')
                        if symbol and symbol != 'INIT':
                            prices[symbol] = data.get('price', 0)
            
            if len(prices) == len(self.symbols):
                return prices
        except Exception as e:
            print(f"Warning: Could not load last prices: {e}")
        
        return None
    
    def generate_stock_tick(self, symbol):
        """Generate a new stock tick with realistic price movement"""
        # Random price change between -2% and +2%
        change_percent = random.uniform(-0.02, 0.02)
        self.prices[symbol] *= (1 + change_percent)
        
        # Random volume between 100 and 10000
        volume = random.randint(100, 10000)
        
        return {
            "symbol": symbol,
            "price": round(self.prices[symbol], 2),
            "volume": volume,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def generate_batch(self):
        """Generate one batch of data for all symbols"""
        batch_data = []
        for symbol in self.symbols:
            tick = self.generate_stock_tick(symbol)
            batch_data.append(tick)
        
        batch_filename = os.path.join(self.output_path, f"batch_{self.batch_num}.json")
        with open(batch_filename, 'w') as f:
            for tick in batch_data:
                f.write(json.dumps(tick) + '\n')
        
        # Print status
        prices_str = ", ".join([f"{s}: ${self.prices[s]:.2f}" for s in self.symbols])
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Batch {self.batch_num} - {prices_str}")
        
        self.batch_num += 1
    
    def run(self, interval=10):
        """Run the producer continuously"""
        self.running = True
        print("="*70)
        print("REAL-TIME STOCK DATA PRODUCER")
        print("="*70)
        print(f"Generating new data every {interval} seconds...")
        print(f"Starting from batch {self.batch_num}")
        print(f"Output directory: {self.output_path}")
        print(f"Symbols: {', '.join(self.symbols)}")
        print("="*70)
        print("Press Ctrl+C to stop")
        print()
        
        try:
            while self.running:
                self.generate_batch()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n" + "="*70)
            print("Stopping producer...")
            print(f"Generated {self.batch_num} batches total")
            print("="*70)
            self.running = False

if __name__ == '__main__':
    producer = RealTimeStockProducer()
    producer.run(interval=5)  # Generate new data every 5 seconds


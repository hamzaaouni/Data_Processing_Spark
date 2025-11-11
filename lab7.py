# ============================================================================
# COMPLETE APACHE SPARK STREAMING LAB - FIXED VERSION
# ============================================================================
# FIXED: Cross-platform compatibility for Windows/Linux/Mac
# PREREQUISITES:
#   1. Install Java 8 or 11 (set JAVA_HOME environment variable)
#   2. Install PySpark: py -m pip install pyspark findspark (Windows)
#                   or: pip install pyspark findspark (Linux/Mac)
#   3. Run: py lab7.py (Windows) or python3 lab7.py (Linux/Mac)

# ============================================================================
# PART 1: ENVIRONMENT SETUP
# ============================================================================
print("="*70)
print("PART 1: ENVIRONMENT SETUP")
print("="*70)

import os
import sys
from pathlib import Path

# Get script directory for relative paths
SCRIPT_DIR = Path(__file__).parent.absolute()
STOCK_STREAM_DIR = SCRIPT_DIR / "stock_stream"

# Check for Java - check process, user, and system environment variables
java_home = os.environ.get("JAVA_HOME")

# On Windows, also check system and user environment variables
if not java_home and sys.platform == "win32":
    try:
        import winreg
        # Check User environment variables
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
            java_home, _ = winreg.QueryValueEx(key, "JAVA_HOME")
            winreg.CloseKey(key)
        except (FileNotFoundError, OSError):
            pass
        
        # Check System environment variables if still not found
        if not java_home:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
                java_home, _ = winreg.QueryValueEx(key, "JAVA_HOME")
                winreg.CloseKey(key)
            except (FileNotFoundError, OSError):
                pass
    except ImportError:
        pass  # winreg not available (shouldn't happen on Windows)

if not java_home:
    # Try to find Java automatically
    import shutil
    java_path = shutil.which("java")
    if java_path:
        # Extract JAVA_HOME from java path
        java_exe = Path(java_path)
        if sys.platform == "win32":
            # On Windows, java.exe is in bin/, so go up one level
            java_home = str(java_exe.parent.parent)
        else:
            # On Unix, java is in bin/, so go up one level
            java_home = str(java_exe.parent.parent)
        os.environ["JAVA_HOME"] = java_home
        print(f"✓ Found Java at: {java_home}")
    else:
        # Try common Java installation paths on Windows
        if sys.platform == "win32":
            common_paths = [
                r"C:\Program Files\Java\jdk-11",
                r"C:\Program Files\Java\jdk-17",
                r"C:\Program Files\Java\jdk-8",
                r"C:\Program Files\Java\jdk1.8.0_*",
                r"C:\Program Files (x86)\Java\jdk-11",
                r"C:\Program Files (x86)\Java\jdk-17",
                r"C:\Program Files (x86)\Java\jdk-8",
            ]
            for base_path in [r"C:\Program Files\Java", r"C:\Program Files (x86)\Java"]:
                if Path(base_path).exists():
                    jdk_dirs = [d for d in Path(base_path).iterdir() if d.is_dir() and (d.name.startswith("jdk") or d.name.startswith("java"))]
                    if jdk_dirs:
                        java_home = str(jdk_dirs[0])
                        print(f"✓ Found Java installation at: {java_home}")
                        break
        
        if not java_home:
            print("⚠️  WARNING: JAVA_HOME not set and Java not found in PATH")
            print("   Please install Java 8 or 11 and set JAVA_HOME environment variable")
            print("   Download from: https://adoptium.net/ or https://www.oracle.com/java/")
            sys.exit(1)

# Set JAVA_HOME in current process environment
if java_home:
    # Fix JAVA_HOME if it incorrectly includes \bin
    java_home_path = Path(java_home)
    if java_home_path.name == "bin":
        java_home = str(java_home_path.parent)
        print(f"✓ Fixed JAVA_HOME (removed \\bin): {java_home}")
    
    os.environ["JAVA_HOME"] = java_home
    print(f"✓ JAVA_HOME: {java_home}")
    
    # Verify Java installation
    java_exe = Path(java_home) / "bin" / "java.exe" if sys.platform == "win32" else Path(java_home) / "bin" / "java"
    if not java_exe.exists():
        print(f"⚠️  WARNING: Java executable not found at {java_exe}")
        print("   JAVA_HOME might be set incorrectly")
    else:
        print(f"✓ Java executable verified: {java_exe}")

# Try to initialize findspark (optional, PySpark can work without it)
try:
    import findspark
    # Try to find Spark if SPARK_HOME not set
    if "SPARK_HOME" not in os.environ:
        # PySpark usually includes Spark, so findspark might find it
        findspark.init()
    else:
        findspark.init()
    print("✓ findspark initialized")
except Exception as e:
    print(f"⚠️  findspark not available (this is usually OK): {e}")

import json
import random
import time
import threading
from datetime import datetime

try:
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F
    from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
    from pyspark.sql.window import Window
    from pyspark.ml.feature import VectorAssembler, StandardScaler
    from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
    from pyspark.ml.evaluation import BinaryClassificationEvaluator
    from pyspark.ml import Pipeline
    print("✓ Libraries imported")
except ImportError as e:
    print(f"❌ ERROR: Failed to import PySpark libraries: {e}")
    print("   Please install: pip install pyspark findspark numpy")
    print("   Or: py -m pip install pyspark findspark numpy")
    sys.exit(1)

# Windows-specific Hadoop workaround
if sys.platform == "win32":
    # Set HADOOP_HOME to avoid winutils.exe requirement
    # Create a dummy hadoop home directory if it doesn't exist
    hadoop_home = SCRIPT_DIR / "hadoop_home" / "bin"
    hadoop_home.mkdir(parents=True, exist_ok=True)
    os.environ["HADOOP_HOME"] = str(hadoop_home.parent)
    os.environ["hadoop.home.dir"] = str(hadoop_home.parent)
    # Set Spark to use local filesystem without native Hadoop
    os.environ["SPARK_LOCAL_IP"] = "localhost"
    
    # Try to create a dummy winutils.exe to avoid errors
    # Note: This is a workaround - a real winutils.exe would be better
    winutils_path = hadoop_home / "winutils.exe"
    if not winutils_path.exists():
        # Create an empty file as placeholder (won't work but prevents some errors)
        try:
            winutils_path.touch()
            print("⚠️  Created placeholder winutils.exe (may still cause issues)")
            print("   For best results, download winutils.exe from:")
            print("   https://github.com/cdarlint/winutils")
        except Exception as e:
            print(f"   Could not create winutils placeholder: {e}")

# Clean up old batch files if they exist
print("🧹 Cleaning up old batch files...")
if STOCK_STREAM_DIR.exists():
    for old_file in STOCK_STREAM_DIR.glob("batch_*.json"):
        try:
            old_file.unlink()
        except Exception as e:
            print(f"   Warning: Could not delete {old_file}: {e}")

try:
    spark_config = SparkSession.builder \
        .appName("FinanceLake-Stock-Analysis") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "2")
    
    # Windows-specific Spark configs to avoid Hadoop native library issues
    if sys.platform == "win32":
        # Force Spark to use Java-based filesystem instead of native Hadoop library
        # This avoids UnsatisfiedLinkError on Windows
        spark_config = spark_config \
            .config("spark.sql.warehouse.dir", str(SCRIPT_DIR / "spark-warehouse")) \
            .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem") \
            .config("spark.hadoop.fs.AbstractFileSystem.file.impl", "org.apache.hadoop.fs.local.LocalFs")
    
    spark = spark_config.getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    print(f"✓ Spark {spark.version} initialized")
except Exception as e:
    print(f"❌ ERROR: Failed to create Spark session: {e}")
    print("   Please ensure Java is installed and JAVA_HOME is set correctly")
    sys.exit(1)

# ============================================================================
# STOCK DATA PRODUCER
# ============================================================================
class StockDataProducer:
    def __init__(self, output_path=None):
        if output_path is None:
            output_path = str(STOCK_STREAM_DIR)
        self.output_path = output_path
        self.symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
        self.prices = {'AAPL': 180.0, 'GOOGL': 140.0, 'MSFT': 370.0, 
                       'AMZN': 145.0, 'TSLA': 240.0}
        os.makedirs(output_path, exist_ok=True)
        self.running = False
        
    def generate_stock_tick(self, symbol):
        change_percent = random.uniform(-0.02, 0.02)
        self.prices[symbol] *= (1 + change_percent)
        volume = random.randint(100, 10000)
        
        return {
            "symbol": symbol,
            "price": round(self.prices[symbol], 2),
            "volume": volume,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def produce_stream(self, duration_seconds=120, interval=2):
        self.running = True
        start_time = time.time()
        batch_num = 0
        
        print(f"🚀 Producer: Generating data for {duration_seconds}s")
        
        while self.running and (time.time() - start_time) < duration_seconds:
            batch_data = []
            for symbol in self.symbols:
                tick = self.generate_stock_tick(symbol)
                batch_data.append(tick)
            
            batch_filename = os.path.join(self.output_path, f"batch_{batch_num}.json")
            with open(batch_filename, 'w') as f:
                for tick in batch_data:
                    f.write(json.dumps(tick) + '\n')
            
            batch_num += 1
            if batch_num % 10 == 0:
                print(f"  ✓ Batch {batch_num}")
            
            time.sleep(interval)
        
        print(f"✓ Producer done: {batch_num} batches")
        self.running = False
    
    def stop(self):
        self.running = False

producer = StockDataProducer()
print("✓ Producer ready")

# ============================================================================
# PART 2: SPARK STRUCTURED STREAMING
# ============================================================================
print("\n" + "="*70)
print("PART 2: STRUCTURED STREAMING")
print("="*70)

# CRITICAL FIX: Proper schema with correct timestamp format
stock_schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("volume", IntegerType(), True),
    StructField("timestamp", StringType(), True)
])
print("✓ Schema defined")

# Ensure streaming directory exists and is accessible
STOCK_STREAM_DIR.mkdir(parents=True, exist_ok=True)

# Create an initial JSON file so Spark can read the directory without native library issues
# This avoids the UnsatisfiedLinkError when Spark tries to list an empty directory
initial_file = STOCK_STREAM_DIR / "initial.json"
if not initial_file.exists():
    # Create a minimal valid JSON file with one record
    initial_data = {
        "symbol": "INIT",
        "price": 100.0,
        "volume": 0,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(initial_file, 'w') as f:
        f.write(json.dumps(initial_data) + '\n')
    print("✓ Created initial JSON file to avoid Hadoop native library issues")

# Use absolute path (file:// URI can cause issues, so use regular path)
stream_path = str(STOCK_STREAM_DIR.absolute())

# Create streaming DataFrame
# Use pathGlobFilter and latestFirst to avoid directory listing issues on Windows
try:
    streaming_df = spark.readStream \
        .format("json") \
        .schema(stock_schema) \
        .option("maxFilesPerTrigger", 2) \
        .option("pathGlobFilter", "batch_*.json") \
        .option("latestFirst", "false") \
        .load(stream_path)
except Exception as e:
    if "UnsatisfiedLinkError" in str(e) or "NativeIO" in str(e):
        print("\n❌ ERROR: Hadoop native library issue on Windows")
        print("   Solution: Download winutils.exe and place it in:")
        print(f"   {hadoop_home / 'winutils.exe'}")
        print("   Download from: https://github.com/cdarlint/winutils")
        print("   Or use WSL (Windows Subsystem for Linux) to run this script")
        sys.exit(1)
    else:
        raise

# CRITICAL FIX: Proper timestamp conversion (capital M for minutes)
streaming_df = streaming_df.withColumn(
    "event_time",
    F.to_timestamp(F.col("timestamp"), "yyyy-MM-dd HH:mm:ss")
)

print("✓ Streaming DataFrame created")

# Agrégation glissante par fenêtre temporelle de 10 secondes
windowed_agg = streaming_df \
    .withWatermark("event_time", "20 seconds") \
    .groupBy(
        F.window(F.col("event_time"), "10 seconds"),  # Fenêtre de 10 secondes comme requis
        F.col("symbol")
    ) \
    .agg(
        F.avg("price").alias("avg_price"),
        F.stddev("price").alias("volatility"),
        F.sum("volume").alias("total_volume"),
        F.count("*").alias("tick_count"),
        F.min("price").alias("min_price"),
        F.max("price").alias("max_price")
    ) \
    .select(
        F.col("window.start").alias("window_start"),
        F.col("window.end").alias("window_end"),
        F.col("symbol"),
        F.col("avg_price"),
        F.col("volatility"),
        F.col("total_volume"),
        F.col("tick_count"),
        F.col("min_price"),
        F.col("max_price")
    )

print("✓ Windowed aggregations (10s windows - agrégation glissante)")

# Start streaming query
query = windowed_agg \
    .writeStream \
    .outputMode("complete") \
    .format("memory") \
    .queryName("stock_aggregations") \
    .trigger(processingTime="3 seconds") \
    .start()

print(f"✓ Query started: {query.id}")

# Start producer in background thread
def run_producer():
    time.sleep(3)
    producer.produce_stream(duration_seconds=120, interval=2)

producer_thread = threading.Thread(target=run_producer, daemon=True)
producer_thread.start()

# CRITICAL FIX: Wait longer for data to actually accumulate
print("\n⏳ Waiting 45 seconds for data accumulation...")
print("   (Producer generates batches every 2s)")
time.sleep(45)

# Check if we have data
record_count = spark.sql("SELECT COUNT(*) as cnt FROM stock_aggregations").collect()[0]['cnt']
print(f"\n✓ Data accumulated: {record_count} aggregated records")

if record_count > 0:
    print("\n📊 Streaming Results:")
    spark.sql("""
        SELECT 
            symbol,
            window_start,
            ROUND(avg_price, 2) as avg_price,
            ROUND(volatility, 2) as volatility,
            total_volume,
            tick_count
        FROM stock_aggregations
        ORDER BY window_start DESC, symbol
        LIMIT 15
    """).show(truncate=False)
else:
    print("⚠️  No data yet, waiting another 20 seconds...")
    time.sleep(20)
    record_count = spark.sql("SELECT COUNT(*) as cnt FROM stock_aggregations").collect()[0]['cnt']
    print(f"✓ Now have: {record_count} records")

# ============================================================================
# PART 3: SPARK SQL ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("PART 3: SPARK SQL ANALYSIS")
print("="*70)

time.sleep(20)  # More accumulation

# Créer une vue temporaire explicite à partir du DataFrame agrégé en streaming
print("\n📋 Création d'une vue temporaire à partir des données agrégées...")
aggregated_df = spark.sql("SELECT * FROM stock_aggregations")
aggregated_df.createOrReplaceTempView("stock_aggregations_view")
print("✓ Vue temporaire 'stock_aggregations_view' créée")

print("\n1️⃣ Statistiques de synthèse (prix moyen et volatilité moyenne par symbole):")
query1 = spark.sql("""
    SELECT 
        symbol,
        ROUND(AVG(avg_price), 2) as overall_avg_price,
        ROUND(AVG(volatility), 2) as overall_volatility,
        SUM(total_volume) as total_volume,
        COUNT(*) as windows
    FROM stock_aggregations_view
    GROUP BY symbol
    ORDER BY overall_avg_price DESC
""")
query1.show()

# Comparaison avec et sans cache()
print("\n2️⃣ Comparaison avec et sans cache():")
print("\n   a) Sans cache() - première exécution:")
start_time = time.time()
result_no_cache = spark.sql("""
    SELECT 
        symbol,
        ROUND(AVG(avg_price), 2) as avg_price,
        ROUND(AVG(volatility), 2) as avg_volatility
    FROM stock_aggregations_view
    GROUP BY symbol
""")
result_no_cache.show()
time_no_cache_1 = time.time() - start_time

print("\n   b) Sans cache() - deuxième exécution (même requête):")
start_time = time.time()
result_no_cache.show()  # Re-exécution
time_no_cache_2 = time.time() - start_time

print("\n   c) Avec cache() - première exécution:")
start_time = time.time()
result_with_cache = spark.sql("""
    SELECT 
        symbol,
        ROUND(AVG(avg_price), 2) as avg_price,
        ROUND(AVG(volatility), 2) as avg_volatility
    FROM stock_aggregations_view
    GROUP BY symbol
""").cache()
result_with_cache.show()  # Force materialization
time_with_cache_1 = time.time() - start_time

print("\n   d) Avec cache() - deuxième exécution (données en cache):")
start_time = time.time()
result_with_cache.show()  # Utilise le cache
time_with_cache_2 = time.time() - start_time

print(f"\n   ⏱️  Temps d'exécution:")
print(f"      Sans cache - 1ère exécution: {time_no_cache_1:.4f}s")
print(f"      Sans cache - 2ème exécution: {time_no_cache_2:.4f}s")
print(f"      Avec cache - 1ère exécution: {time_with_cache_1:.4f}s")
print(f"      Avec cache - 2ème exécution: {time_with_cache_2:.4f}s")
if time_with_cache_2 < time_no_cache_2:
    speedup = time_no_cache_2 / time_with_cache_2 if time_with_cache_2 > 0 else 0
    print(f"      ✓ Amélioration avec cache: {speedup:.2f}x plus rapide")

# Analyse du plan d'exécution avec .explain('formatted')
print("\n3️⃣ Analyse du plan d'exécution avec Catalyst Optimizer:")
print("\n   Plan d'exécution SANS cache (formatted):")
explain_query = spark.sql("""
    SELECT 
        symbol,
        ROUND(AVG(avg_price), 2) as avg_price,
        ROUND(AVG(volatility), 2) as avg_volatility
    FROM stock_aggregations_view
    GROUP BY symbol
""")
explain_query.explain('formatted')

print("\n   Plan d'exécution AVEC cache (formatted):")
explain_query_cached = spark.sql("""
    SELECT 
        symbol,
        ROUND(AVG(avg_price), 2) as avg_price,
        ROUND(AVG(volatility), 2) as avg_volatility
    FROM stock_aggregations_view
    GROUP BY symbol
""").cache()
explain_query_cached.explain('formatted')

print("\n4️⃣ Most Volatile Windows:")
query2 = spark.sql("""
    SELECT 
        symbol,
        window_start,
        ROUND(volatility, 2) as volatility,
        ROUND(avg_price, 2) as avg_price
    FROM stock_aggregations_view
    WHERE volatility IS NOT NULL
    ORDER BY volatility DESC
    LIMIT 5
""")
query2.show(truncate=False)

print("\n5️⃣ Price Ranges:")
query3 = spark.sql("""
    SELECT 
        symbol,
        ROUND(MIN(min_price), 2) as lowest,
        ROUND(MAX(max_price), 2) as highest,
        ROUND(MAX(max_price) - MIN(min_price), 2) as range
    FROM stock_aggregations_view
    GROUP BY symbol
    ORDER BY range DESC
""")
query3.show()

# ============================================================================
# PART 4: MACHINE LEARNING
# ============================================================================
print("\n" + "="*70)
print("PART 4: MACHINE LEARNING")
print("="*70)

time.sleep(25)  # Let more data accumulate

print("\n📥 Collecting ML training data...")
training_data = spark.sql("""
    SELECT * FROM stock_aggregations_view ORDER BY symbol, window_start
""")

ml_record_count = training_data.count()
print(f"✓ Training records: {ml_record_count}")

if ml_record_count < 20:
    print("⚠️  Need more data, waiting 30 more seconds...")
    time.sleep(30)
    training_data = spark.sql("""
        SELECT * FROM stock_aggregations_view ORDER BY symbol, window_start
    """)
    ml_record_count = training_data.count()
    print(f"✓ Now have: {ml_record_count} records")

if ml_record_count >= 20:
    # Feature engineering
    print("\n🔧 Engineering features...")
    window_spec = Window.partitionBy("symbol").orderBy("window_start")
    
    feature_df = training_data \
        .withColumn("prev_price", F.lag("avg_price", 1).over(window_spec)) \
        .withColumn("prev_volume", F.lag("total_volume", 1).over(window_spec)) \
        .withColumn("price_change", F.col("avg_price") - F.col("prev_price")) \
        .withColumn("volume_change", F.col("total_volume") - F.col("prev_volume")) \
        .withColumn("price_range", F.col("max_price") - F.col("min_price")) \
        .withColumn("price_volatility", 
                    F.when(F.col("volatility").isNull(), 0).otherwise(F.col("volatility"))) \
        .filter(F.col("prev_price").isNotNull())
    
    feature_df = feature_df.withColumn("price_increase", 
                    F.when(F.col("price_change") > 0, 1.0).otherwise(0.0))
    
    ml_data = feature_df.select(
        "symbol", "avg_price", "price_volatility", "total_volume",
        "price_range", "price_change", "volume_change", "price_increase"
    )
    
    ml_count = ml_data.count()
    print(f"✓ Feature engineered: {ml_count} samples")
    
    if ml_count >= 10:
        print("\n📊 Sample features:")
        ml_data.show(5, truncate=False)
        
        # Define features
        feature_cols = ["avg_price", "price_volatility", "total_volume",
                       "price_range", "price_change", "volume_change"]
        
        # Pipeline components
        assembler = VectorAssembler(
            inputCols=feature_cols,
            outputCol="features_raw",
            handleInvalid="skip"
        )
        
        scaler = StandardScaler(
            inputCol="features_raw",
            outputCol="features",
            withStd=True,
            withMean=True
        )
        
        # Split data
        train_data, test_data = ml_data.randomSplit([0.8, 0.2], seed=42)
        train_count = train_data.count()
        test_count = test_data.count()
        
        print(f"\nTrain: {train_count} | Test: {test_count}")
        
        if train_count >= 5 and test_count >= 2:
            # Logistic Regression
            print("\n📈 Training Logistic Regression...")
            lr = LogisticRegression(
                featuresCol="features",
                labelCol="price_increase",
                maxIter=100,
                regParam=0.01
            )
            
            lr_pipeline = Pipeline(stages=[assembler, scaler, lr])
            lr_model = lr_pipeline.fit(train_data)
            lr_predictions = lr_model.transform(test_data)
            
            evaluator = BinaryClassificationEvaluator(
                labelCol="price_increase",
                metricName="areaUnderROC"
            )
            
            lr_auc = evaluator.evaluate(lr_predictions)
            lr_accuracy = lr_predictions.filter(
                F.col("price_increase") == F.col("prediction")
            ).count() / test_count
            
            print(f"✓ LR: AUC={lr_auc:.4f}, Accuracy={lr_accuracy:.4f}")
            
            # Random Forest
            print("\n🌳 Training Random Forest...")
            rf = RandomForestClassifier(
                featuresCol="features",
                labelCol="price_increase",
                numTrees=20,
                maxDepth=5,
                seed=42
            )
            
            rf_pipeline = Pipeline(stages=[assembler, scaler, rf])
            rf_model = rf_pipeline.fit(train_data)
            rf_predictions = rf_model.transform(test_data)
            
            rf_auc = evaluator.evaluate(rf_predictions)
            rf_accuracy = rf_predictions.filter(
                F.col("price_increase") == F.col("prediction")
            ).count() / test_count
            
            print(f"✓ RF: AUC={rf_auc:.4f}, Accuracy={rf_accuracy:.4f}")
            
            # Feature importance
            rf_trained = rf_model.stages[-1]
            feature_importance = rf_trained.featureImportances.toArray()
            print("\n🎯 Feature Importance:")
            for feat, imp in sorted(zip(feature_cols, feature_importance), 
                                   key=lambda x: x[1], reverse=True):
                print(f"  {feat:20s}: {imp:.4f}")
            
            # Comparison
            print("\n🏆 Model Comparison:")
            comparison = spark.createDataFrame([
                ("Logistic Regression", lr_auc, lr_accuracy),
                ("Random Forest", rf_auc, rf_accuracy)
            ], ["Model", "AUC", "Accuracy"])
            comparison.show(truncate=False)
        else:
            print(f"⚠️  Not enough data for train/test split")
    else:
        print(f"⚠️  Only {ml_count} samples after feature engineering")
else:
    print(f"⚠️  Only {ml_record_count} records - need at least 20 for ML")

# ============================================================================
# PART 5: VALUE AT RISK
# ============================================================================
print("\n" + "="*70)
print("PART 5: VALUE AT RISK ANALYSIS")
print("="*70)

var_df = spark.sql("""
    SELECT 
        symbol,
        ROUND(AVG(volatility), 4) as avg_volatility,
        ROUND(AVG(avg_price), 2) as avg_price,
        ROUND(1.645 * AVG(volatility), 4) as VaR_95
    FROM stock_aggregations_view
    WHERE volatility IS NOT NULL
    GROUP BY symbol
    ORDER BY VaR_95 DESC
""")

print("\n💰 Value at Risk (95% Confidence):")
var_df.show()

# ============================================================================
# CLEANUP
# ============================================================================
print("\n" + "="*70)
print("🏁 STOPPING STREAMING QUERY")
print("="*70)

try:
    query.stop()
    print("✓ Streaming query stopped")
except Exception as e:
    print(f"⚠️  Error stopping query: {e}")

try:
    producer.stop()
    print("✓ Producer stopped")
except Exception as e:
    print(f"⚠️  Error stopping producer: {e}")

try:
    final_count = spark.sql("SELECT COUNT(*) as cnt FROM stock_aggregations").collect()[0]['cnt']
    print(f"\n✅ LAB COMPLETE!")
    print(f"   Final aggregated records: {final_count}")
except Exception as e:
    print(f"\n⚠️  Could not get final count: {e}")

try:
    spark.stop()
    print("✓ Spark session stopped")
except Exception as e:
    print(f"⚠️  Error stopping Spark: {e}")

print("="*70)
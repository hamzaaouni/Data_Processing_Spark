# Dockerfile for Apache Spark Streaming Lab
FROM python:3.11-slim

# Install Java 17 (required for Spark)
# Download and install OpenJDK 17 directly
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download and install OpenJDK 17 from Adoptium
RUN wget -q https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.13%2B11/OpenJDK17U-jdk_x64_linux_hotspot_17.0.13_11.tar.gz \
    && mkdir -p /usr/lib/jvm \
    && tar -xzf OpenJDK17U-jdk_x64_linux_hotspot_17.0.13_11.tar.gz -C /usr/lib/jvm \
    && rm OpenJDK17U-jdk_x64_linux_hotspot_17.0.13_11.tar.gz \
    && ln -s /usr/lib/jvm/jdk-17.0.13+11 /usr/lib/jvm/java-17-openjdk

# Set JAVA_HOME (use the symlink for compatibility)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk
ENV PATH=$PATH:$JAVA_HOME/bin

# Install PySpark and dependencies
RUN pip install --no-cache-dir pyspark findspark numpy pandas matplotlib seaborn

# Set working directory
WORKDIR /app

# Copy lab files
COPY lab7.py /app/
COPY visualize_results.py /app/
COPY README.md /app/

# Create directories for streaming data and visualizations
RUN mkdir -p /app/stock_stream /app/spark-warehouse /app/visualizations

# Expose Spark UI port (optional)
EXPOSE 4040

# Run the lab script
CMD ["python", "lab7.py"]


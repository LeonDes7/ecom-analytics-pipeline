# Using the Official Apache Spark image (Spark 4.0.2 is current for 2026)
FROM apache/spark:4.0.2

USER root
# Install Python dependencies for your pipeline
# Note: Official images already have Python, we just add your extra tools
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create the project directory and set permissions
WORKDIR /opt/spark/project
RUN chown -R spark:spark /opt/spark/project

USER spark
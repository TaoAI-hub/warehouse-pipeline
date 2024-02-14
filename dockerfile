 Use the official Apache Airflow image as the base image
FROM apache/airflow:latest

# Set environment variables (optional, adjust as needed)
ENV AIRFLOW_HOME=/usr/local/airflow

# Install any additional dependencies required by your DAGs
# For example, if you need to install psycopg2 for PostgreSQL connections:
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    && apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
USER airflow

# Copy your DAGs, plugins, and any other necessary files into the container
COPY dags/ $AIRFLOW_HOME/dags/
COPY plugins/ $AIRFLOW_HOME/plugins/
# Add any other necessary COPY commands for additional files

# Expose the Airflow web server port
EXPOSE 8080

# Start Airflow web server (by default)
CMD ["webserver"]

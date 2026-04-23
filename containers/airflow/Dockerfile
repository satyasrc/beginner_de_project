FROM apache/airflow:2.10.3-python3.11
COPY requirements.txt /
# FIX 2: Switch to 'airflow' user to install Python packages securely
USER airflow
# FIX 3: Removed '--user' because Airflow's Python environment doesn't allow user-site packages inside its virtualenv
RUN pip install --no-cache-dir -r /requirements.txt

# FIX 4: Switch to 'root' to run system installation scripts (like Quarto)
USER root
COPY quarto.sh /
RUN cd / && bash /quarto.sh

# --- PERMISSION FIX FOR QUARTO ---
# Assuming quarto installs to /opt/quarto (the standard location). 
# We give all users (a+rx) read and execute access.
# If your script installs it somewhere else, change '/opt/quarto' to that path.
RUN if [ -d "/opt/quarto" ]; then chmod -R a+rx /opt/quarto; fi

# Find the location of the airflow executable and give it execute permissions
# (This ensures the .local directory is accessible)
RUN chmod -R a+rx /home/airflow/.local

# Switch back to airflow for the final setup
USER airflow

# Copy your setup script to AIRFLOW_HOME
COPY setup_conn.py $AIRFLOW_HOME
# USER root

# install missing ps command
USER root
RUN apt-get update && apt-get install -y procps 

# install JAVA and set JAVA_HOME
RUN apt-get update && apt-get install -y openjdk-17-jdk
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH=$JAVA_HOME/bin:$PATH

# We use a bind mount to extract the tarball without adding the 400MB file to the image layers
RUN --mount=type=bind,source=spark-3.5.1-bin-hadoop3.tgz,target=/tmp/spark.tgz \
    mkdir -p /opt/spark && tar xvzf /tmp/spark.tgz --directory /opt/spark --strip-components=1

# set spark paths
ENV SPARK_HOME='/opt/spark'
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

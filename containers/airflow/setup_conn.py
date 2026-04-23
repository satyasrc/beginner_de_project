import subprocess
import json
import sys
import shutil

# Locate airflow binary
airflow_bin = shutil.which("airflow") or "/home/airflow/.local/bin/airflow"

# Define connection details
conn_id = "aws_default"
conn_type = "aws"
access_key = "minio"
secret_key = "minio123"
region_name = "us-east-1"
endpoint_url = "http://minio:9000"
# Construct the extra JSON
extra = {
    "aws_access_key_id": access_key,
    "aws_secret_access_key": secret_key,
    "region_name": region_name,
    "endpoint_url": endpoint_url,
}
# Convert to JSON string
extra_json = json.dumps(extra)

# Execute the command using sys.executable with the airflow script
subprocess.run([
    sys.executable, airflow_bin, "connections", "add", conn_id,
    "--conn-type", conn_type,
    "--conn-extra", extra_json
])


def add_airflow_connection():
    connection_id = "spark-conn"
    connection_type = "spark"
    host = "spark://192.168.0.1"
    port = "7077"
    
    # Execute the command using sys.executable with the airflow script
    result = subprocess.run([
        sys.executable, airflow_bin, "connections", "add", connection_id,
        "--conn-host", host,
        "--conn-type", connection_type,
        "--conn-port", port
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Successfully added {connection_id} connection")
    else:
        print(f"Failed to add {connection_id} connection: {result.stderr}")

# Add the airflow connection
add_airflow_connection()
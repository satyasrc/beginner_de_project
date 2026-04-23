import os
import shutil
import pytest
from unittest import mock

import sys
# sys.modules["boto3"] = mock.Mock()
sys.modules["duckdb"] = mock.Mock()

from dags.user_analytics import get_s3_folder

@pytest.fixture
def mock_boto3_resource(monkeypatch):
    mock_bucket = mock.Mock()
    mock_bucket.objects.filter.return_value = [
        mock.Mock(key="folder/file1.txt"),
        mock.Mock(key="folder/sub/file2.txt"),
    ]
    mock_s3 = mock.Mock()
    mock_s3.Bucket.return_value = mock_bucket
    monkeypatch.setattr("boto3.resource", lambda *a, **kw: mock_s3)
    return mock_bucket

def test_get_s3_folder_downloads_files(tmp_path, mock_boto3_resource, monkeypatch):
    # Setup
    s3_bucket = "test-bucket"
    s3_folder = "folder"
    local_folder = tmp_path / "local"
    os.makedirs(local_folder, exist_ok=True)

    # Patch os.path.exists and shutil.rmtree
    monkeypatch.setattr(os.path, "exists", lambda path: False)
    monkeypatch.setattr(shutil, "rmtree", lambda path: None)
    # monkeypatch.setattr(os, "makedirs", lambda path, exist_ok: None)

    # Patch bucket.download_file to just touch the file
    def fake_download_file(key, target):
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w") as f:
            f.write("test")
    mock_boto3_resource.download_file.side_effect = fake_download_file

    # Run
    get_s3_folder(s3_bucket, s3_folder, str(local_folder))

    # Assert download_file called for each object
    assert mock_boto3_resource.download_file.call_count == 2

def test_get_s3_folder_removes_existing_folder(monkeypatch, mock_boto3_resource):
    s3_bucket = "test-bucket"
    s3_folder = "folder"
    local_folder = "/tmp/local"
    # Patch os.path.exists to True to trigger rmtree
    monkeypatch.setattr(os.path, "exists", lambda path: True)
    rmtree_called = {}
    monkeypatch.setattr(shutil, "rmtree", lambda path: rmtree_called.setdefault("called", True))
    monkeypatch.setattr(os, "makedirs", lambda path, exist_ok: None)
    mock_boto3_resource.download_file.side_effect = lambda key, target: None

    get_s3_folder(s3_bucket, s3_folder, local_folder)
    assert rmtree_called.get("called", False)

def test_create_user_behaviour_metric_duckdb(monkeypatch, tmp_path):
    # Patch duckdb.sql and its write_csv
    mock_duckdb_sql = mock.Mock()
    monkeypatch.setattr("duckdb.sql", lambda q: mock_duckdb_sql)
    mock_duckdb_sql.write_csv = mock.Mock()

    # Patch time.sleep to avoid delay
    monkeypatch.setattr("time.sleep", lambda s: None)

    # Import and call the function
    from dags.user_analytics import create_user_behaviour_metric
    create_user_behaviour_metric()

    # Assert write_csv called with correct path
    mock_duckdb_sql.write_csv.assert_called_once_with("/opt/airflow/data/behaviour_metrics.csv")
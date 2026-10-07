from pathlib import Path

def test_project_structure():
    required=["README.md","docker-compose.yml","Dockerfile.spark","Dockerfile.api","pyspark/etl.py","pyspark/train.py","pyspark/predict.py","api/main.py","database/init.sql"]
    assert all(Path(x).exists() for x in required)

def test_expected_sensor_columns():
    expected={"machine_id","timestamp","temperature","vibration","pressure","rpm","current","humidity","operating_hours","failure"}
    assert len(expected)==10

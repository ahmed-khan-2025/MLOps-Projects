from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from collector.config import (
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
)


def get_engine() -> Engine:
    """
    Create a PostgreSQL SQLAlchemy engine using pg8000.

    pg8000 is a pure-Python PostgreSQL driver and avoids
    the Windows native DLL issue encountered with psycopg.
    """

    database_url = (
        f"postgresql+pg8000://"
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    return create_engine(
        database_url,
        pool_pre_ping=True,
    )


def get_connection():
    """
    Create a database connection.
    """

    engine = get_engine()

    return engine.connect()


def init_database():
    """
    Create the required PostgreSQL tables and indexes.
    """

    measurements_table = """
    CREATE TABLE IF NOT EXISTS grid_measurements (
        id SERIAL PRIMARY KEY,

        timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),

        voltage DOUBLE PRECISION NOT NULL,
        current DOUBLE PRECISION NOT NULL,
        frequency DOUBLE PRECISION NOT NULL,

        active_power DOUBLE PRECISION NOT NULL,
        reactive_power DOUBLE PRECISION NOT NULL,

        power_factor DOUBLE PRECISION NOT NULL,
        voltage_angle DOUBLE PRECISION NOT NULL
    );
    """

    predictions_table = """
    CREATE TABLE IF NOT EXISTS stability_predictions (
        id SERIAL PRIMARY KEY,

        measurement_id INTEGER NOT NULL
            REFERENCES grid_measurements(id)
            ON DELETE CASCADE,

        timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),

        stability_class VARCHAR(20) NOT NULL,
        stability_probability DOUBLE PRECISION NOT NULL,

        anomaly_status VARCHAR(20) NOT NULL,
        anomaly_score DOUBLE PRECISION NOT NULL,

        risk_score DOUBLE PRECISION NOT NULL,
        risk_level VARCHAR(20) NOT NULL,

        explanation TEXT
    );
    """

    indexes = [
        """
        CREATE INDEX IF NOT EXISTS idx_grid_measurements_timestamp
        ON grid_measurements(timestamp DESC);
        """,

        """
        CREATE INDEX IF NOT EXISTS idx_stability_predictions_timestamp
        ON stability_predictions(timestamp DESC);
        """,

        """
        CREATE INDEX IF NOT EXISTS idx_stability_predictions_measurement
        ON stability_predictions(measurement_id);
        """,
    ]

    engine = get_engine()

    with engine.begin() as connection:

        connection.execute(
            text(measurements_table)
        )

        connection.execute(
            text(predictions_table)
        )

        for index in indexes:
            connection.execute(
                text(index)
            )

    print("PostgreSQL database initialized successfully.")


def insert_measurement(measurement):
    """
    Insert one industrial measurement.

    Returns:
        int: ID of the inserted measurement.
    """

    query = """
    INSERT INTO grid_measurements (
        timestamp,
        voltage,
        current,
        frequency,
        active_power,
        reactive_power,
        power_factor,
        voltage_angle
    )
    VALUES (
        :timestamp,
        :voltage,
        :current,
        :frequency,
        :active_power,
        :reactive_power,
        :power_factor,
        :voltage_angle
    )
    RETURNING id;
    """

    engine = get_engine()

    with engine.begin() as connection:

        result = connection.execute(
            text(query),
            {
                "timestamp": measurement["timestamp"],
                "voltage": measurement["voltage"],
                "current": measurement["current"],
                "frequency": measurement["frequency"],
                "active_power": measurement["active_power"],
                "reactive_power": measurement["reactive_power"],
                "power_factor": measurement["power_factor"],
                "voltage_angle": measurement["voltage_angle"],
            },
        )

        measurement_id = result.scalar_one()

    return measurement_id


def insert_prediction(measurement_id, prediction):
    """
    Insert ML prediction for a measurement.

    Returns:
        int: ID of the inserted prediction.
    """

    query = """
    INSERT INTO stability_predictions (
        measurement_id,
        stability_class,
        stability_probability,
        anomaly_status,
        anomaly_score,
        risk_score,
        risk_level,
        explanation
    )
    VALUES (
        :measurement_id,
        :stability_class,
        :stability_probability,
        :anomaly_status,
        :anomaly_score,
        :risk_score,
        :risk_level,
        :explanation
    )
    RETURNING id;
    """

    engine = get_engine()

    with engine.begin() as connection:

        result = connection.execute(
            text(query),
            {
                "measurement_id": measurement_id,
                "stability_class": prediction["stability_class"],
                "stability_probability": prediction["stability_probability"],
                "anomaly_status": prediction["anomaly_status"],
                "anomaly_score": prediction["anomaly_score"],
                "risk_score": prediction["risk_score"],
                "risk_level": prediction["risk_level"],
                "explanation": prediction["explanation"],
            },
        )

        prediction_id = result.scalar_one()

    return prediction_id


def fetch_latest_measurement():
    """
    Return the latest grid measurement.
    """

    query = """
    SELECT *
    FROM grid_measurements
    ORDER BY timestamp DESC
    LIMIT 1;
    """

    engine = get_engine()

    with engine.connect() as connection:

        result = connection.execute(
            text(query)
        )

        row = result.mappings().first()

        return dict(row) if row else None


def fetch_measurements(limit=100):
    """
    Return recent grid measurements.
    """

    query = """
    SELECT *
    FROM grid_measurements
    ORDER BY timestamp DESC
    LIMIT :limit;
    """

    engine = get_engine()

    with engine.connect() as connection:

        result = connection.execute(
            text(query),
            {"limit": limit},
        )

        return [
            dict(row)
            for row in result.mappings().all()
        ]


def fetch_latest_prediction():
    """
    Return the latest ML prediction.
    """

    query = """
    SELECT
        p.*,
        m.timestamp AS measurement_timestamp
    FROM stability_predictions p
    JOIN grid_measurements m
        ON p.measurement_id = m.id
    ORDER BY p.timestamp DESC
    LIMIT 1;
    """

    engine = get_engine()

    with engine.connect() as connection:

        result = connection.execute(
            text(query)
        )

        row = result.mappings().first()

        return dict(row) if row else None


def fetch_predictions(limit=100):
    """
    Return recent ML predictions.
    """

    query = """
    SELECT
        p.*,
        m.timestamp AS measurement_timestamp
    FROM stability_predictions p
    JOIN grid_measurements m
        ON p.measurement_id = m.id
    ORDER BY p.timestamp DESC
    LIMIT :limit;
    """

    engine = get_engine()

    with engine.connect() as connection:

        result = connection.execute(
            text(query),
            {"limit": limit},
        )

        return [
            dict(row)
            for row in result.mappings().all()
        ]


if __name__ == "__main__":
    init_database()
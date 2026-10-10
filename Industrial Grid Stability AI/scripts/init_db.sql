CREATE TABLE IF NOT EXISTS grid_measurements (
 id BIGSERIAL PRIMARY KEY,
 timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 voltage DOUBLE PRECISION NOT NULL,
 current DOUBLE PRECISION NOT NULL,
 frequency DOUBLE PRECISION NOT NULL,
 active_power DOUBLE PRECISION NOT NULL,
 reactive_power DOUBLE PRECISION NOT NULL,
 power_factor DOUBLE PRECISION NOT NULL,
 voltage_angle DOUBLE PRECISION NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_grid_measurements_timestamp ON grid_measurements(timestamp DESC);
CREATE TABLE IF NOT EXISTS stability_predictions (
 id BIGSERIAL PRIMARY KEY,
 measurement_id BIGINT NOT NULL REFERENCES grid_measurements(id) ON DELETE CASCADE,
 timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
 stability_class VARCHAR(30) NOT NULL,
 stability_probability DOUBLE PRECISION NOT NULL,
 anomaly_status VARCHAR(30) NOT NULL,
 anomaly_score DOUBLE PRECISION NOT NULL,
 risk_score DOUBLE PRECISION NOT NULL,
 risk_level VARCHAR(30) NOT NULL,
 explanation TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_stability_predictions_timestamp ON stability_predictions(timestamp DESC);

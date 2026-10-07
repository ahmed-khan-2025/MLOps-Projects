CREATE TABLE IF NOT EXISTS machine_predictions (
    id SERIAL PRIMARY KEY,
    machine_id VARCHAR(100),
    prediction INTEGER NOT NULL,
    failure_probability DOUBLE PRECISION NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    temperature DOUBLE PRECISION,
    vibration DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    rpm DOUBLE PRECISION,
    current DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    operating_hours DOUBLE PRECISION,
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_machine_predictions_machine_id ON machine_predictions(machine_id);
CREATE INDEX IF NOT EXISTS idx_machine_predictions_predicted_at ON machine_predictions(predicted_at);

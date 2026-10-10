# AI-Assisted Automated Stability Assessment for Industrial Grids

Industrial AI/MLOps pipeline: **Beckhoff TwinCAT PLC -> ADS -> Python -> PostgreSQL -> Random Forest + Isolation Forest -> FastAPI -> Prometheus/Grafana**.

The PLC generates simulated electrical-grid operating conditions; no physical sensors are required.

## Measurements

Voltage, current, frequency, active power, reactive power, power factor and voltage angle.

## ML

- Random Forest: STABLE / WARNING / UNSTABLE
- Isolation Forest: anomaly detection
- Risk engine: 0-100 stability risk score

## Run on Windows

```powershell
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
docker compose up -d postgres
python -m ml.generate_training_data
python -m ml.train_stability_model
python -m ml.train_anomaly_model
$env:MOCK_MODE="true"
python -m collector.main
```

In another terminal:

```powershell
.venv\Scripts\activate
uvicorn api.main:app --reload --port 8005
```

Open `http://localhost:8005/docs`.

For dashboards, start:

```powershell
docker compose up -d prometheus grafana
```

Grafana: `http://localhost:3002` (admin/admin)

Prometheus: `http://localhost:9090`

## TwinCAT mode

After TwinCAT PLC is configured and running, set:

```powershell
$env:MOCK_MODE="false"
$env:PLC_AMS_NET_ID="YOUR_AMS_NET_ID"
$env:PLC_PORT="851"
python -m collector.main
```

Do not use a guessed AMS Net ID. Use the AMS Net ID shown by your TwinCAT installation.

## API

- `/health`
- `/api/measurements/latest`
- `/api/measurements`
- `/api/stability/latest`
- `/api/stability`
- `/api/anomalies/latest`
- `/metrics`

## Safety

This is a software/simulation portfolio project, not a certified electrical protection or grid-control system.

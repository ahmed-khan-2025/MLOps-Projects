import os
import subprocess
import time
from pathlib import Path

import pandas as pd
import psycopg
from scipy.stats import ks_2samp
from prometheus_client import Gauge, start_http_server


# ============================================================
# CONFIGURATION
# ============================================================

DB = os.getenv("DATABASE_URL")
REF = Path(os.getenv("REFERENCE_PATH"))

WINDOW = int(os.getenv("DRIFT_WINDOW"))
PVALUE = float(os.getenv("DRIFT_P_VALUE"))
COOLDOWN = int(os.getenv("RETRAIN_COOLDOWN_SECONDS"))


# ============================================================
# PROMETHEUS METRICS
# ============================================================

drift = Gauge(
    "ml_data_drift_detected",
    "1 if drift detected",
)

pvalue = Gauge(
    "ml_data_drift_p_value",
    "KS test p-value",
)

retrain = Gauge(
    "ml_retraining_total",
    "Successful automated retraining count",
)


# ============================================================
# GET RECENT READINGS
# ============================================================

def readings():
    with psycopg.connect(DB) as conn:
        return [
            r[0]
            for r in conn.execute(
                """
                SELECT temperature
                FROM temperature_readings
                ORDER BY timestamp DESC
                LIMIT %s
                """,
                (WINDOW,),
            ).fetchall()
        ]


# ============================================================
# RETRAIN MODEL
# ============================================================

def train():
    result = subprocess.run(
        ["python", "-m", "ml.train"],
        text=True,
    )

    return result.returncode == 0


# ============================================================
# MONITOR
# ============================================================

def main():

    # Prometheus metrics available on port 8001
    start_http_server(8001)

    count = 0
    last = 0

    while True:

        try:

            # ------------------------------------------------
            # Current production readings
            # ------------------------------------------------

            current = readings()

            # ------------------------------------------------
            # Reference training data
            # ------------------------------------------------

            reference = (
                pd.read_csv(REF)["temperature"]
                .dropna()
                .tolist()
                if REF.exists()
                else []
            )

            # ------------------------------------------------
            # Drift detection
            # ------------------------------------------------

            if len(current) >= 20 and len(reference) >= 20:

                stat, p = ks_2samp(
                    reference,
                    current,
                )

                is_drift = p < PVALUE

                drift.set(
                    int(is_drift)
                )

                pvalue.set(
                    float(p)
                )

                print(
                    f"KS={stat:.4f} "
                    f"p={p:.6f} "
                    f"drift={is_drift}"
                )

                # ------------------------------------------------
                # Automatic retraining
                # ------------------------------------------------

                now = time.time()

                if (
                    is_drift
                    and now - last >= COOLDOWN
                ):

                    if train():

                        count += 1

                        retrain.set(
                            count
                        )

                        last = now

        except Exception as exc:

            print(
                "monitor:",
                exc
            )

        time.sleep(30)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()

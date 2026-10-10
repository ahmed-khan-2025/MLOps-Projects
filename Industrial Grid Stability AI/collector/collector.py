import time
import traceback

from collector.ads_client import (
    TwinCATADSClient,
    MockGridClient,
)

from collector.config import (
    MOCK_MODE,
    COLLECT_INTERVAL_SECONDS,
)

from collector.database import (
    insert_measurement,
    insert_prediction,
)

from collector.predictor import StabilityPredictor


def create_client():
    """Create the TwinCAT or mock data client."""

    if MOCK_MODE:
        print("Running in MOCK mode")
        return MockGridClient()

    print("Running in TwinCAT ADS mode")
    return TwinCATADSClient()


def main():
    """Run the continuous industrial grid collector."""

    print("=" * 70)
    print("Industrial Grid Stability AI Collector")
    print("=" * 70)

    client = None

    try:
        # Create TwinCAT ADS client
        client = create_client()

        # Load ML models once
        print("Loading ML models...")

        predictor = StabilityPredictor()

        print("ML models loaded successfully")
        print(
            f"Collection interval: "
            f"{COLLECT_INTERVAL_SECONDS} seconds"
        )

        print()
        print("Collector started.")
        print("Press CTRL+C to stop.")
        print()

        while True:

            try:
                # -------------------------------------------------
                # 1. Read measurement from TwinCAT
                # -------------------------------------------------

                measurement = client.read_measurement()

                print(
                    f"Voltage={measurement['voltage']:.4f} | "
                    f"Current={measurement['current']:.2f} | "
                    f"Frequency={measurement['frequency']:.3f} | "
                    f"ActivePower={measurement['active_power']:.2f}"
                )

                # -------------------------------------------------
                # 2. Save measurement to PostgreSQL
                # -------------------------------------------------

                measurement_id = insert_measurement(
                    measurement
                )

                # -------------------------------------------------
                # 3. Run ML prediction
                # -------------------------------------------------

                prediction = predictor.predict(
                    measurement
                )

                # -------------------------------------------------
                # 4. Save prediction to PostgreSQL
                # -------------------------------------------------

                prediction_id = insert_prediction(
                    measurement_id,
                    prediction
                )

                # -------------------------------------------------
                # 5. Display prediction
                # -------------------------------------------------

                print(
                    f"Measurement ID: {measurement_id} | "
                    f"Prediction ID: {prediction_id}"
                )

                print(
                    f"Stability: "
                    f"{prediction['stability_class']} "
                    f"({prediction['stability_probability']:.2%})"
                )

                print(
                    f"Anomaly: "
                    f"{prediction['anomaly_status']} | "
                    f"Score: "
                    f"{prediction['anomaly_score']:.2f}"
                )

                print(
                    f"Risk: "
                    f"{prediction['risk_score']:.2f} | "
                    f"Level: "
                    f"{prediction['risk_level']}"
                )

                print(
                    f"Explanation: "
                    f"{prediction['explanation']}"
                )

                print("-" * 70)

            except Exception as exc:

                print(
                    f"Collection error: {exc}"
                )

                traceback.print_exc()

            time.sleep(
                COLLECT_INTERVAL_SECONDS
            )

    except KeyboardInterrupt:

        print()
        print("Collector stopped by user.")

    except Exception as exc:

        print(
            f"Fatal collector error: {exc}"
        )

        traceback.print_exc()

    finally:

        if client is not None:
            client.close()

        print(
            "Collector shutdown complete."
        )


if __name__ == "__main__":
    main()


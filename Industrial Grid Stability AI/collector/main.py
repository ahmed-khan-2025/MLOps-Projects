
import time
import traceback

from collector.ads_client import MockGridClient, TwinCATADSClient
from collector.config import MOCK_MODE, COLLECT_INTERVAL_SECONDS
from collector.database import insert_measurement, insert_prediction
from collector.predictor import StabilityPredictor


def main():
    client = MockGridClient() if MOCK_MODE else TwinCATADSClient()
    predictor = StabilityPredictor()

    print("Collector started. MOCK_MODE=", MOCK_MODE)

    try:
        while True:
            try:
                m = client.read_measurement()
                mid = insert_measurement(m)
                p = predictor.predict(m)
                insert_prediction(mid, p)

                print(
                    f"V={m['voltage']:.3f} "
                    f"F={m['frequency']:.2f} "
                    f"I={m['current']:.1f} "
                    f"PF={m['power_factor']:.2f} "
                    f"{p['stability_class']} "
                    f"Risk={p['risk_score']:.1f}"
                )

            except Exception:
                traceback.print_exc()

            time.sleep(COLLECT_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("Stopped.")

    finally:
        client.close()


if __name__ == "__main__":
    main()


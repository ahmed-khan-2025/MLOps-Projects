from pathlib import Path

import joblib
import numpy as np

from collector.config import (
    STABILITY_MODEL_PATH,
    ANOMALY_MODEL_PATH,
)

from ml.features import feature_row


class StabilityPredictor:
    """
    Industrial grid stability prediction service.

    Combines:
    1. Random Forest stability classification
    2. Isolation Forest anomaly detection
    3. Engineering-based risk scoring
    4. Human-readable explanations
    """

    def __init__(self):
        self.stability_model_path = Path(
            STABILITY_MODEL_PATH
        )

        self.anomaly_model_path = Path(
            ANOMALY_MODEL_PATH
        )

        self._load_models()

    def _load_models(self):
        """Load the trained ML models."""

        if not self.stability_model_path.exists():
            raise FileNotFoundError(
                f"Stability model not found: "
                f"{self.stability_model_path}"
            )

        if not self.anomaly_model_path.exists():
            raise FileNotFoundError(
                f"Anomaly model not found: "
                f"{self.anomaly_model_path}"
            )

        # ==================================================
        # Stability model
        # ==================================================

        stability_bundle = joblib.load(
            self.stability_model_path
        )

        if isinstance(stability_bundle, dict):
            self.model = stability_bundle["model"]
            self.classes = stability_bundle["classes"]
        else:
            self.model = stability_bundle
            self.classes = self.model.classes_

        # ==================================================
        # Anomaly model
        # ==================================================

        anomaly_bundle = joblib.load(
            self.anomaly_model_path
        )

        if isinstance(anomaly_bundle, dict):
            self.anomaly = anomaly_bundle["model"]
        else:
            self.anomaly = anomaly_bundle

        print(
            f"Stability model loaded: "
            f"{self.stability_model_path}"
        )

        print(
            f"Anomaly model loaded: "
            f"{self.anomaly_model_path}"
        )

    # ======================================================
    # Anomaly score calibration
    # ======================================================

    def _calculate_anomaly_score(
        self,
        raw_anomaly_score,
        anomaly_prediction,
    ):
        """
        Convert the Isolation Forest decision value
        into an intuitive 0-100 anomaly severity score.

        Interpretation:

            0-30   = normal
            30-70  = borderline / elevated
            70-100 = anomaly

        Isolation Forest:

            positive decision value
                -> more normal

            negative decision value
                -> more anomalous
        """

        raw_score = float(
            raw_anomaly_score
        )

        # --------------------------------------------------
        # Normal observation
        # --------------------------------------------------

        if anomaly_prediction == 1:

            # Strongly normal observations should be
            # close to zero.

            if raw_score >= 0.05:

                score = 10.0

            # Normal but closer to the decision boundary.
            elif raw_score >= 0.0:

                score = 10.0 + (
                    (0.05 - raw_score)
                    / 0.05
                ) * 20.0

            else:

                score = 30.0

        # --------------------------------------------------
        # Anomalous observation
        # --------------------------------------------------

        else:

            # Isolation Forest negative values indicate
            # increasingly abnormal observations.

            severity = (
                (-raw_score) / 0.20
            )

            severity = float(
                np.clip(
                    severity,
                    0.0,
                    1.0,
                )
            )

            score = (
                70.0
                + severity * 30.0
            )

        return float(
            np.clip(
                score,
                0.0,
                100.0,
            )
        )

    # ======================================================
    # Main prediction
    # ======================================================

    def predict(self, measurement):
        """
        Generate stability, anomaly, and risk predictions.
        """

        # ==================================================
        # Feature preparation
        # ==================================================

        X = feature_row(
            measurement
        )

        # ==================================================
        # Stability prediction
        # ==================================================

        predicted_class = self.model.predict(
            X
        )[0]

        probabilities = self.model.predict_proba(
            X
        )[0]

        probability_map = {
            int(cls): float(prob)
            for cls, prob in zip(
                self.classes,
                probabilities,
            )
        }

        stability_class_map = {
            0: "STABLE",
            1: "WARNING",
            2: "UNSTABLE",
        }

        stability_class = stability_class_map.get(
            int(predicted_class),
            str(predicted_class),
        )

        stability_probability = probability_map.get(
            int(predicted_class),
            float(
                max(probabilities)
            ),
        )

        # ==================================================
        # Anomaly detection
        # ==================================================

        raw_anomaly_score = float(
            self.anomaly.decision_function(
                X
            )[0]
        )

        anomaly_prediction = int(
            self.anomaly.predict(
                X
            )[0]
        )

        if anomaly_prediction == -1:
            anomaly_status = "ANOMALY"
        else:
            anomaly_status = "NORMAL"

        # Convert raw Isolation Forest score
        # into intuitive 0-100 severity.
        anomaly_score = (
            self._calculate_anomaly_score(
                raw_anomaly_score,
                anomaly_prediction,
            )
        )

        # ==================================================
        # Engineering measurements
        # ==================================================

        voltage = float(
            measurement["voltage"]
        )

        current = float(
            measurement["current"]
        )

        frequency = float(
            measurement["frequency"]
        )

        power_factor = float(
            measurement["power_factor"]
        )

        # ==================================================
        # Engineering deviations
        # ==================================================

        voltage_deviation = abs(
            voltage - 1.0
        )

        frequency_deviation = abs(
            frequency - 50.0
        )

        current_deviation = abs(
            (current - 100.0) / 100.0
        )

        power_factor_deviation = abs(
            power_factor - 0.95
        )

        # ==================================================
        # Engineering score
        # ==================================================

        voltage_score = np.clip(
            voltage_deviation / 0.15 * 100,
            0,
            100,
        )

        frequency_score = np.clip(
            frequency_deviation / 1.0 * 100,
            0,
            100,
        )

        current_score = np.clip(
            current_deviation / 1.0 * 100,
            0,
            100,
        )

        power_factor_score = np.clip(
            (0.95 - power_factor) / 0.40 * 100,
            0,
            100,
        )

        engineering_score = float(
            np.mean(
                [
                    voltage_score,
                    frequency_score,
                    current_score,
                    power_factor_score,
                ]
            )
        )

        # ==================================================
        # Instability probability
        # ==================================================

        instability_probability = float(
            probability_map.get(
                2,
                0.0,
            )
            + 0.5
            * probability_map.get(
                1,
                0.0,
            )
        )

        # ==================================================
        # Overall risk score
        # ==================================================

        risk_score = float(
            100
            * (
                0.60
                * instability_probability
                + 0.20
                * (
                    anomaly_score
                    / 100
                )
                + 0.20
                * (
                    engineering_score
                    / 100
                )
            )
        )

        risk_score = float(
            np.clip(
                risk_score,
                0,
                100,
            )
        )

        # --------------------------------------------------
        # Minimum risk for ML warning states
        # --------------------------------------------------

        if stability_class == "UNSTABLE":

            risk_score = max(
                risk_score,
                80.0,
            )

        elif stability_class == "WARNING":

            risk_score = max(
                risk_score,
                45.0,
            )

        # ==================================================
        # Risk level
        # ==================================================

        if risk_score <= 30:

            risk_level = "LOW"

        elif risk_score <= 60:

            risk_level = "MODERATE"

        elif risk_score <= 80:

            risk_level = "HIGH"

        else:

            risk_level = "CRITICAL"

        # ==================================================
        # Explanation
        # ==================================================

        explanation_parts = []

        if voltage_deviation > 0.05:

            explanation_parts.append(
                "Voltage deviation is high"
            )

        if frequency_deviation > 0.30:

            explanation_parts.append(
                "Frequency deviation is high"
            )

        if current > 130:

            explanation_parts.append(
                "Current is high"
            )

        if power_factor < 0.85:

            explanation_parts.append(
                "Power factor is degraded"
            )

        if power_factor < 0.70:

            explanation_parts.append(
                "Power factor is severely degraded"
            )

        if anomaly_status == "ANOMALY":

            explanation_parts.append(
                "Anomalous operating behavior detected"
            )

        if stability_class == "WARNING":

            explanation_parts.append(
                "ML model indicates a warning state"
            )

        if stability_class == "UNSTABLE":

            explanation_parts.append(
                "ML model indicates an unstable grid state"
            )

        if not explanation_parts:

            explanation_parts.append(
                "Operating measurements are within "
                "the expected range"
            )

        explanation = (
            "; ".join(
                explanation_parts
            )
            + "."
        )

        # ==================================================
        # Final prediction
        # ==================================================

        return {
            "stability_class": stability_class,

            "stability_probability": float(
                stability_probability
            ),

            "anomaly_status": anomaly_status,

            "anomaly_score": float(
                anomaly_score
            ),

            "risk_score": float(
                risk_score
            ),

            "risk_level": risk_level,

            "explanation": explanation,
        }

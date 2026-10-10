from datetime import datetime, timezone
import random

import pyads

from collector.config import PLC_AMS_NET_ID, PLC_PORT


class TwinCATADSClient:
    """
    Real TwinCAT ADS client.

    Reads industrial grid measurements from the TwinCAT PLC
    through ADS using pyads.
    """

    def __init__(self):
        self.plc = pyads.Connection(
            PLC_AMS_NET_ID,
            PLC_PORT,
        )

        self.plc.open()

        print("Connected to TwinCAT via ADS")
        print(f"AMS Net ID: {PLC_AMS_NET_ID}")
        print(f"PLC Port: {PLC_PORT}")

    def read_measurement(self):
        """
        Read one measurement from TwinCAT.
        """

        return {
            "timestamp": datetime.now(timezone.utc),

            "voltage": float(
                self.plc.read_by_name(
                    "GVL.Voltage",
                    pyads.PLCTYPE_REAL,
                )
            ),

            "current": float(
                self.plc.read_by_name(
                    "GVL.Current",
                    pyads.PLCTYPE_REAL,
                )
            ),

            "frequency": float(
                self.plc.read_by_name(
                    "GVL.Frequency",
                    pyads.PLCTYPE_REAL,
                )
            ),

            "active_power": float(
                self.plc.read_by_name(
                    "GVL.ActivePower",
                    pyads.PLCTYPE_REAL,
                )
            ),

            "reactive_power": float(
                self.plc.read_by_name(
                    "GVL.ReactivePower",
                    pyads.PLCTYPE_REAL,
                )
            ),

            "power_factor": float(
                self.plc.read_by_name(
                    "GVL.PowerFactor",
                    pyads.PLCTYPE_REAL,
                )
            ),

            "voltage_angle": float(
                self.plc.read_by_name(
                    "GVL.VoltageAngle",
                    pyads.PLCTYPE_REAL,
                )
            ),
        }

    def close(self):
        """
        Close the ADS connection safely.
        """

        try:
            if self.plc.is_open:
                self.plc.close()

            print("TwinCAT ADS connection closed")

        except Exception as exc:
            print(f"Error closing ADS connection: {exc}")


class MockGridClient:
    """
    Mock industrial grid client.

    Used for local development and testing when TwinCAT
    is not available.
    """

    def __init__(self):
        self.t = 0

    def read_measurement(self):
        """
        Generate simulated industrial measurements.
        """

        self.t += 1

        phase = (self.t // 20) % 3

        # ------------------------------------------
        # Normal / stable operation
        # ------------------------------------------

        if phase == 0:

            values = (
                1.0 + random.uniform(-0.01, 0.01),
                100.0 + random.uniform(-5, 5),
                50.0 + random.uniform(-0.05, 0.05),
                70.0 + random.uniform(-4, 4),
                20.0 + random.uniform(-2, 2),
                0.96 + random.uniform(-0.01, 0.01),
                random.uniform(-1, 1),
            )

        # ------------------------------------------
        # Warning operation
        # ------------------------------------------

        elif phase == 1:

            values = (
                0.945 + random.uniform(-0.015, 0.015),
                145.0 + random.uniform(-8, 8),
                49.5 + random.uniform(-0.12, 0.12),
                90.0 + random.uniform(-5, 5),
                40.0 + random.uniform(-4, 4),
                0.82 + random.uniform(-0.025, 0.025),
                4.0 + random.uniform(-1, 1),
            )

        # ------------------------------------------
        # Unstable operation
        # ------------------------------------------

        else:

            values = (
                0.87 + random.uniform(-0.02, 0.02),
                190.0 + random.uniform(-10, 10),
                48.7 + random.uniform(-0.2, 0.2),
                110.0 + random.uniform(-6, 6),
                65.0 + random.uniform(-6, 6),
                0.66 + random.uniform(-0.035, 0.035),
                8.0 + random.uniform(-1.5, 1.5),
            )

        return {
            "timestamp": datetime.now(timezone.utc),

            "voltage": values[0],
            "current": values[1],
            "frequency": values[2],
            "active_power": values[3],
            "reactive_power": values[4],

            "power_factor": max(
                0.4,
                min(1.0, values[5]),
            ),

            "voltage_angle": values[6],
        }

    def close(self):
        """
        Mock client does not require cleanup.
        """


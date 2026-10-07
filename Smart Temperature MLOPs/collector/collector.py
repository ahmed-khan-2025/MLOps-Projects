import asyncio
import os
import time
from datetime import datetime, timezone

import psycopg
from asyncua import Client


# ============================================================
# CONFIGURATION
# ============================================================

DB = os.getenv("DATABASE_URL")
ENDPOINT = os.getenv("OPCUA_ENDPOINT")
NODE_ID = os.getenv("OPCUA_NODE_ID")


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db():
    with psycopg.connect(DB) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS temperature_readings (
                id BIGSERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                temperature DOUBLE PRECISION NOT NULL
            )
            """
        )
        conn.commit()


# ============================================================
# SAVE TEMPERATURE
# ============================================================

def save(value):
    with psycopg.connect(DB) as conn:
        conn.execute(
            """
            INSERT INTO temperature_readings(
                timestamp,
                temperature
            )
            VALUES (%s, %s)
            """,
            (
                datetime.now(timezone.utc),
                value,
            ),
        )
        conn.commit()


# ============================================================
# OPC UA COLLECTOR
# ============================================================

async def main():

    init_db()

    while True:
        try:
            async with Client(url=ENDPOINT) as client:

                node = client.get_node(NODE_ID)

                print("Connected to OPC UA.")

                while True:

                    value = float(
                        await node.read_value()
                    )

                    save(value)

                    print(
                        f"stored={value:.2f} C"
                    )

                    await asyncio.sleep(1)

        except Exception as exc:

            print(
                "collector:",
                exc
            )

            time.sleep(5)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())

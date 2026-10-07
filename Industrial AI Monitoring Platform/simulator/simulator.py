import random
import time

import requests


API_URL = "http://backend:8000/api/machines/readings"


MACHINES = [
    "MACHINE-001",
    "MACHINE-002",
    "MACHINE-003",
    "MACHINE-004",
    "MACHINE-005",
]


def generate_sensor_data(machine_id: str):
    """
    Generate simulated industrial sensor data.
    """

    temperature = random.gauss(65, 8)
    vibration = random.gauss(2.5, 0.5)
    pressure = random.gauss(5, 0.4)
    rpm = random.gauss(1500, 120)
    current = random.gauss(8, 1)
    humidity = random.gauss(50, 8)

    # Occasionally create abnormal
    # operating conditions.
    if random.random() < 0.05:
        temperature += random.uniform(15, 25)
        vibration += random.uniform(1, 2)

    return {
        "machine_id": machine_id,
        "temperature": round(
            temperature,
            2,
        ),
        "vibration": round(
            max(vibration, 0),
            2,
        ),
        "pressure": round(
            pressure,
            2,
        ),
        "rpm": round(
            max(rpm, 0),
            2,
        ),
        "current": round(
            max(current, 0),
            2,
        ),
        "humidity": round(
            max(humidity, 0),
            2,
        ),
    }


def send_reading(data):
    """
    Send one sensor reading
    to the FastAPI backend.
    """

    try:

        response = requests.post(
            API_URL,
            json=data,
            timeout=5,
        )

        print(
            f"{data['machine_id']} | "
            f"HTTP {response.status_code} | "
            f"T={data['temperature']}°C | "
            f"V={data['vibration']} | "
            f"RPM={data['rpm']}"
        )

    except requests.RequestException as exc:

        print(
            f"Backend unavailable: {exc}"
        )


def main():

    print(
        "Industrial AI Machine Simulator started."
    )

    print(
        f"Machines: {', '.join(MACHINES)}"
    )

    while True:

        for machine_id in MACHINES:

            data = generate_sensor_data(
                machine_id
            )

            send_reading(data)

        time.sleep(2)


if __name__ == "__main__":
    main()
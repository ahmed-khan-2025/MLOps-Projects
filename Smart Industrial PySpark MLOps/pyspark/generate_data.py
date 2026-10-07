from pathlib import Path
import csv, math, random
from datetime import datetime, timedelta

random.seed(42)
output = Path("/app/data/raw/machine_sensor_data.csv")
output.parent.mkdir(parents=True, exist_ok=True)
rows = []
start = datetime(2026, 1, 1)

for machine_number in range(1, 21):
    machine_id = f"M-{machine_number:03d}"
    operating_hours = random.uniform(500, 9000)
    for i in range(250):
        ts = start + timedelta(minutes=10 * i)
        temperature = 55 + 7 * math.sin(i / 20) + random.gauss(0, 2)
        vibration = 2 + 0.6 * math.sin(i / 15) + random.gauss(0, 0.25)
        pressure = 100 + 4 * math.sin(i / 25) + random.gauss(0, 1.5)
        rpm = 1500 + random.gauss(0, 90)
        current = 10 + random.gauss(0, 0.8)
        humidity = 55 + random.gauss(0, 5)
        score = sum([
            temperature > 70,
            vibration > 3,
            pressure > 105,
            current > 11.5,
            operating_hours > 7500,
        ])
        failure = int(score >= 2)
        if random.random() < 0.04:
            temperature += random.uniform(12, 25)
            vibration += random.uniform(1, 3)
            failure = 1
        rows.append([machine_id, ts.isoformat(), round(temperature,3), round(vibration,3), round(pressure,3), round(rpm,3), round(current,3), round(humidity,3), round(operating_hours,3), failure])

columns = ["machine_id","timestamp","temperature","vibration","pressure","rpm","current","humidity","operating_hours","failure"]
with output.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f); writer.writerow(columns); writer.writerows(rows)
print(f"Generated {len(rows)} rows: {output}")

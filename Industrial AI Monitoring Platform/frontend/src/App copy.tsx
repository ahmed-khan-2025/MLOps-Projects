import { useEffect, useState } from "react";

import Header from "./components/Header";
import SensorCard from "./components/SensorCard";
import MachineStatus from "./components/MachineStatus";
import TemperatureChart from "./components/TemperatureChart";

import { getReadings } from "./api";
import type { SensorReading } from "./types";

function App() {
  const [readings, setReadings] = useState<SensorReading[]>([]);
  const [error, setError] = useState("");

  const machineId = "MACHINE-001";

  useEffect(() => {
    let mounted = true;

    const loadData = async () => {
      try {
        const data = await getReadings(machineId);

        console.log("READINGS FROM API:", data);
        console.log("NUMBER OF READINGS:", data.length);

        if (mounted) {
          setReadings(data);
          setError("");
        }
      } catch (err) {
        console.error("API ERROR:", err);

        if (mounted) {
          setError("Could not connect to the backend.");
        }
      }
    };

    loadData();

    const interval = setInterval(loadData, 2000);

    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  if (error) {
    return (
      <div className="loading">
        <h2>{error}</h2>
        <p>Backend: http://localhost:8004</p>
      </div>
    );
  }

  if (readings.length === 0) {
    return (
      <div className="loading">
        <h2>Waiting for machine data...</h2>
        <p>Machine: {machineId}</p>
        <p>Readings received: 0</p>
      </div>
    );
  }

  const latest = readings[0];

  return (
    <div className="app">
      <Header />

      <main>
        <div className="machine-header">
          <div>
            <h2>{machineId}</h2>
            <p>Industrial Production Machine</p>
            <p>Readings received: {readings.length}</p>
          </div>
        </div>

        <section className="sensor-grid">
          <SensorCard
            title="Temperature"
            value={latest.temperature}
            unit="°C"
          />

          <SensorCard
            title="Vibration"
            value={latest.vibration}
            unit="mm/s"
          />

          <SensorCard
            title="Pressure"
            value={latest.pressure}
            unit="bar"
          />

          <SensorCard
            title="RPM"
            value={latest.rpm}
            unit="rpm"
          />

          <SensorCard
            title="Current"
            value={latest.current}
            unit="A"
          />

          <SensorCard
            title="Humidity"
            value={latest.humidity}
            unit="%"
          />
        </section>

        <section className="main-grid">
          <TemperatureChart readings={readings} />

          <MachineStatus
            probability={latest.failure_probability ?? 0}
          />
        </section>
      </main>
    </div>
  );
}

export default App;
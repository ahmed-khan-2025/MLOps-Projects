import { useEffect, useState } from "react";

import Header from "./components/Header";
import SensorCard from "./components/SensorCard";
import MachineStatus from "./components/MachineStatus";
import TemperatureChart from "./components/TemperatureChart";

import { getReadings } from "./api";
import type { SensorReading } from "./types";

function App() {
  const [readings, setReadings] = useState<SensorReading[]>([]);
  const [selectedMachine, setSelectedMachine] =
    useState("MACHINE-001");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const machines = [
    "MACHINE-001",
    "MACHINE-002",
    "MACHINE-003",
    "MACHINE-004",
    "MACHINE-005",
  ];

  useEffect(() => {
    const loadData = async () => {
      try {
        setError("");

        const data = await getReadings(selectedMachine);

        console.log(
          "Selected machine:",
          selectedMachine
        );

        console.log(
          "Number of readings:",
          data.length
        );

        setReadings(data);
        setLoading(false);
      } catch (err) {
        console.error(
          "Unable to load sensor data:",
          err
        );

        setError(
          "Unable to connect to the Industrial AI backend."
        );

        setLoading(false);
      }
    };

    loadData();

    const interval = setInterval(
      loadData,
      2000
    );

    return () => {
      clearInterval(interval);
    };
  }, [selectedMachine]);

  const latest = readings[0];

  if (loading && !latest) {
    return (
      <div className="loading">
        Loading machine data...
      </div>
    );
  }

  if (error && !latest) {
    return (
      <div className="loading">
        <h2>Industrial AI Monitoring</h2>
        <p>{error}</p>

        <button
          onClick={() =>
            window.location.reload()
          }
        >
          Retry
        </button>
      </div>
    );
  }

  if (!latest) {
    return (
      <div className="loading">
        <h2>No data available</h2>

        <p>
          Waiting for {selectedMachine} sensor data...
        </p>
      </div>
    );
  }

  return (
    <div className="app">

      <Header />

      <main>

        {/* MACHINE SELECTOR */}

        <div className="machine-header">

          <div>
            <h2>Industrial Machine</h2>

            <p>
              Select a machine to monitor
              real-time sensor data and ML
              predictions.
            </p>
          </div>

          <div className="machine-selector">

            <label htmlFor="machine-select">
              Select Machine
            </label>

            <select
              id="machine-select"
              value={selectedMachine}
              onChange={(event) => {
                setSelectedMachine(
                  event.target.value
                );

                setReadings([]);
                setLoading(true);
              }}
            >

              {machines.map((machine) => (
                <option
                  key={machine}
                  value={machine}
                >
                  {machine}
                </option>
              ))}

            </select>

          </div>

        </div>

        {/* MACHINE INFORMATION */}

        <div className="machine-info">

          <div>
            <strong>Machine ID</strong>
            <span>{selectedMachine}</span>
          </div>

          <div>
            <strong>Data Points</strong>
            <span>{readings.length}</span>
          </div>

          <div>
            <strong>Connection</strong>
            <span>LIVE</span>
          </div>

        </div>

        {/* SENSOR CARDS */}

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

        {/* CHART + ML STATUS */}

        <section className="main-grid">

          <TemperatureChart
            readings={readings}
          />

          <MachineStatus
            probability={
              latest.failure_probability ?? 0
            }
          />

        </section>

      </main>

    </div>
  );
}

export default App;
import { useEffect, useState } from "react";

import Header from "./components/Header";
import SensorCard from "./components/SensorCard";
import MachineStatus from "./components/MachineStatus";
import TemperatureChart from "./components/TemperatureChart";

import { getMachines, getReadings } from "./api";
import type { SensorReading } from "./types";

function App() {
  const [machines, setMachines] = useState<string[]>([]);
  const [selectedMachine, setSelectedMachine] = useState("");
  const [readings, setReadings] = useState<SensorReading[]>([]);
  const [loadingMachines, setLoadingMachines] = useState(true);
  const [loadingReadings, setLoadingReadings] = useState(false);
  const [error, setError] = useState("");

  // ============================================================
  // LOAD MACHINES
  // ============================================================

  useEffect(() => {
    const loadMachines = async () => {
      try {
        setError("");
        setLoadingMachines(true);

        const machineList = await getMachines();

        console.log("Registered machines:", machineList);

        setMachines(machineList);

        if (machineList.length > 0) {
          setSelectedMachine(machineList[0]);
        } else {
          setError("No registered machines found.");
        }
      } catch (err) {
        console.error(
          "Unable to load machines:",
          err
        );

        setError(
          "Unable to load machines from the backend."
        );
      } finally {
        setLoadingMachines(false);
      }
    };

    loadMachines();
  }, []);

  // ============================================================
  // LOAD READINGS FOR SELECTED MACHINE
  // ============================================================

  useEffect(() => {
    if (!selectedMachine) {
      return;
    }

    const loadData = async () => {
      try {
        setError("");
        setLoadingReadings(true);

        const data = await getReadings(
          selectedMachine
        );

        console.log(
          "Selected machine:",
          selectedMachine
        );

        console.log(
          "Number of readings:",
          data.length
        );

        setReadings(data);
      } catch (err) {
        console.error(
          "Unable to load sensor data:",
          err
        );

        setError(
          `Unable to load data for ${selectedMachine}.`
        );

        setReadings([]);
      } finally {
        setLoadingReadings(false);
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

  // ============================================================
  // INITIAL MACHINE LOADING
  // ============================================================

  if (loadingMachines) {
    return (
      <div className="loading">
        <h2>Industrial AI Monitoring</h2>

        <p>
          Loading registered machines...
        </p>
      </div>
    );
  }

  // ============================================================
  // MACHINE LOAD ERROR
  // ============================================================

  if (
    error &&
    machines.length === 0
  ) {
    return (
      <div className="loading">
        <h2>
          Industrial AI Monitoring
        </h2>

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

  // ============================================================
  // NO MACHINES
  // ============================================================

  if (machines.length === 0) {
    return (
      <div className="loading">
        <h2>
          No Registered Machines
        </h2>

        <p>
          No machines are currently
          registered in the system.
        </p>
      </div>
    );
  }

  const latest = readings[0];

  // ============================================================
  // DASHBOARD
  // ============================================================

  return (
    <div className="app">

      <Header />

      <main>

        {/* ================================================== */}
        {/* MACHINE SELECTOR */}
        {/* ================================================== */}

        <div className="machine-header">

          <div>
            <h2>
              Industrial Machine
            </h2>

            <p>
              Select a registered machine
              to monitor real-time sensor
              data and ML predictions.
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
                setError("");
              }}
            >

              {machines.map(
                (machine) => (
                  <option
                    key={machine}
                    value={machine}
                  >
                    {machine}
                  </option>
                )
              )}

            </select>

          </div>

        </div>

        {/* ================================================== */}
        {/* ERROR */}
        {/* ================================================== */}

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* ================================================== */}
        {/* MACHINE INFORMATION */}
        {/* ================================================== */}

        <div className="machine-info">

          <div>
            <strong>
              Machine ID
            </strong>

            <span>
              {selectedMachine}
            </span>
          </div>

          <div>
            <strong>
              Data Points
            </strong>

            <span>
              {readings.length}
            </span>
          </div>

          <div>
            <strong>
              Connection
            </strong>

            <span>
              LIVE
            </span>
          </div>

        </div>

        {/* ================================================== */}
        {/* LOADING SENSOR DATA */}
        {/* ================================================== */}

        {loadingReadings && !latest && (
          <div className="loading">
            <p>
              Loading sensor data from{" "}
              {selectedMachine}...
            </p>
          </div>
        )}

        {/* ================================================== */}
        {/* NO SENSOR DATA */}
        {/* ================================================== */}

        {!loadingReadings &&
          !error &&
          !latest && (
            <div className="loading">
              <p>
                Waiting for sensor data from{" "}
                {selectedMachine}...
              </p>
            </div>
          )}

        {/* ================================================== */}
        {/* SENSOR DASHBOARD */}
        {/* ================================================== */}

        {latest && (
          <>
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
          </>
        )}

      </main>

    </div>
  );
}

export default App;


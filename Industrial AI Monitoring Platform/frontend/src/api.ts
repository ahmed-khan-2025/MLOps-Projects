import axios from "axios";
import type { SensorReading } from "./types";

const API_URL = "http://localhost:8004";

export const api = axios.create({
  baseURL: API_URL,
});

// ============================================================
// MACHINE API
// ============================================================

export async function getMachines(): Promise<string[]> {
  const response = await api.get<string[]>(
    "/api/machines"
  );

  console.log("MACHINES STATUS:", response.status);
  console.log("REGISTERED MACHINES:", response.data);

  return response.data;
}


// ============================================================
// SENSOR READINGS API
// ============================================================

export async function getReadings(
  machineId: string
): Promise<SensorReading[]> {
  const response = await api.get<SensorReading[]>(
    `/api/machines/${machineId}/readings`
  );

  console.log("READINGS STATUS:", response.status);
  console.log("SELECTED MACHINE:", machineId);
  console.log("READINGS:", response.data);
  console.log("READINGS COUNT:", response.data.length);

  return response.data;
}
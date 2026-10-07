import axios from "axios";
import type { SensorReading } from "./types";

const API_URL = "http://localhost:8004";

export const api = axios.create({
  baseURL: API_URL,
});

export async function getReadings(
  machineId: string
): Promise<SensorReading[]> {
  const response = await api.get<SensorReading[]>(
    `/api/machines/${machineId}/readings`
  );

  console.log("API STATUS:", response.status);
  console.log("API DATA:", response.data);
  console.log("API DATA LENGTH:", response.data.length);

  return response.data;
}
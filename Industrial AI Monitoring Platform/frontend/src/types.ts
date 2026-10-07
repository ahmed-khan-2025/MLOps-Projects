export interface SensorReading {
  id: number;
  machine_id: string;
  timestamp: string;

  temperature: number;
  vibration: number;
  pressure: number;
  rpm: number;
  current: number;
  humidity: number;

  failure_probability: number | null;
}

export interface Prediction {
  failure_probability: number;
  status: string;
}
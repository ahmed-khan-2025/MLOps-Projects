import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import { SensorReading } from "../types";

interface Props {
  readings: SensorReading[];
}

export default function TemperatureChart({
  readings,
}: Props) {
  const data = [...readings]
    .reverse()
    .map((reading) => ({
      time: new Date(
        reading.timestamp
      ).toLocaleTimeString(),

      temperature: reading.temperature,
    }));

  return (
    <div className="chart-card">
      <h2>Temperature</h2>

      <ResponsiveContainer
        width="100%"
        height={300}
      >
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="time" />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="temperature"
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
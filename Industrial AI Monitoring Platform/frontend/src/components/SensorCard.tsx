interface SensorCardProps {
  title: string;
  value: number;
  unit: string;
}

export default function SensorCard({
  title,
  value,
  unit,
}: SensorCardProps) {
  return (
    <div className="sensor-card">
      <div className="sensor-title">{title}</div>

      <div className="sensor-value">
        {value.toFixed(1)}
        <span>{unit}</span>
      </div>
    </div>
  );
}
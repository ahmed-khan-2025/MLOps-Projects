interface MachineStatusProps {
  probability: number;
}

export default function MachineStatus({
  probability,
}: MachineStatusProps) {
  const percentage = probability * 100;

  let status = "NORMAL";

  if (percentage >= 70) {
    status = "CRITICAL";
  } else if (percentage >= 40) {
    status = "WARNING";
  }

  return (
    <div className="status-card">
      <h2>Machine Status</h2>

      <div className="status">
        {status}
      </div>

      <p>
        Failure Risk: {percentage.toFixed(1)}%
      </p>
    </div>
  );
}
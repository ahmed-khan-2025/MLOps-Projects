# TwinCAT PLC

Create a Global Variable List named `GVL`:

```text
Voltage       : REAL := 1.0;
Current       : REAL := 100.0;
Frequency     : REAL := 50.0;
ActivePower   : REAL := 70.0;
ReactivePower : REAL := 20.0;
PowerFactor   : REAL := 0.96;
VoltageAngle  : REAL := 0.0;
```

Use `MAIN.TcPOU` as the PLC program. It cycles STABLE -> WARNING -> UNSTABLE every 20 seconds.

Python reads these symbols through ADS using `pyads`.

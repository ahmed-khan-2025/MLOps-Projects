import asyncio
import math
import random
from asyncua import Server, ua

async def main():
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    idx = await server.register_namespace("http://smart-temperature-mlops")
    machine = await server.nodes.objects.add_object(idx, "Machine")
    temperature = await machine.add_variable(
        ua.NodeId("Machine.Temperature", idx),
        "Temperature",
        55.0,
        ua.VariantType.Double,
    )
    await temperature.set_writable()

    print("OPC UA server: opc.tcp://0.0.0.0:4840/freeopcua/server/")
    print("Node: ns=2;s=Machine.Temperature")

    async with server:
        t = 0
        while True:
            normal = 55 + 4 * math.sin(t / 12)
            heat = 0
            if 45 <= t % 180 <= 80:
                heat = 22 * math.sin((t - 45) / 35 * math.pi)
            value = round(normal + heat + random.gauss(0, 1), 2)
            await temperature.write_value(value)
            print(f"temperature={value:.2f} C")
            t += 1
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())

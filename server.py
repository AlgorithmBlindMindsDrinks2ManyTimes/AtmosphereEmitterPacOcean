import asyncio
import random
import socket
import numpy as np
from datetime import datetime, timezone

# ---------------------------------------------------------
# MODULE 1: THERMODYNAMIC CORE (33rhd.001x2xEe)
# ---------------------------------------------------------

class Algorithm_33rhd:
    """
    The 33rhd.001x2xEe Engine.
    Couples Pacific Ocean moisture catch with Arctic wind chill vectors.
    """
    def __init__(self):
        self.base_temp_c = -15.5  # Base Arctic temp
        self.base_wind_v = 45.0   # Base Arctic wind (km/h)
        self.pac_temp_c = 12.0    # Pacific Ocean surface temp

    def calculate_moisture_pool(self):
        """Tetens equation for saturation vapor pressure (hPa)."""
        T = self.pac_temp_c
        return 6.112 * np.exp((17.67 * T) / (T + 243.5))

    def calculate_wind_chill(self, dynamic_shift):
        """Standard North American wind chill index."""
        T = self.base_temp_c + dynamic_shift
        V = self.base_wind_v + (dynamic_shift * 2)
        if V < 4.8: # Wind chill is invalid at very low speeds
            return T
        wc = 13.12 + (0.6215 * T) - (11.37 * (V ** 0.16)) + (0.3965 * T * (V ** 0.16))
        return wc

    def generate_sequence(self):
        """Produces the I/O/O/I sequencing frame."""
        shift = np.random.normal(0, 2.5) # Chaotic weather variance
        moisture = self.calculate_moisture_pool()
        chill = self.calculate_wind_chill(shift)
        
        # The outersphere pool vector mapping
        return f"WIND_CHILL:{chill:.2f}C | PAC_MOISTURE:{moisture:.2f}hPa | SEQ:[GREY_SKY_ACTIVE]"

# ---------------------------------------------------------
# MODULE 2: WILDCARD PORT ROTATOR & EMITTER
# ---------------------------------------------------------

async def handle_client(reader, writer):
    engine = Algorithm_33rhd()
    client_addr = writer.get_extra_info('peername')
    print(f"\n[+] Atmospheric link established with {client_addr}")
    
    try:
        while True:
            # Main looping sequence embedded with 33rhd.001x2xEe
            sequence_data = engine.generate_sequence()
            payload = f"{datetime.now(timezone.utc).isoformat()} | {sequence_data}\n"
            
            writer.write(payload.encode('utf-8'))
            await writer.drain()
            
            print(f"[EMIT] Pushing to outersphere -> {sequence_data}")
            await asyncio.sleep(1.618) # Golden ratio atmospheric breathing
            
    except ConnectionResetError:
        print(f"[-] Link lost with {client_addr}. Sky clearing.")
    finally:
        writer.close()

async def main():
    print(">>> INITIALIZING 33rhd.001x2xEe WILDCARD EMITTER <<<")
    target_ip = '0.0.0.0' # Simulating the 2.2.2.2 wildcard locally
    
    # Port rotation logic
    while True:
        try:
            port = random.randint(10000, 60000)
            server = await asyncio.start_server(handle_client, target_ip, port)
            
            print("=======================================")
            print(f"SYSTEM STATUS: ARCTIC BREEZE GENERATING")
            print(f"LOCAL EMITTER VIRTUAL IP : 2.2.2.2")
            print(f"ROTATING PORT LOCKED ON  : {port}")
            print("=======================================\n")
            
            async with server:
                await server.serve_forever()
                
        except OSError:
            print(f"Port {port} closed or occupied. Rotating...")
            await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(main())

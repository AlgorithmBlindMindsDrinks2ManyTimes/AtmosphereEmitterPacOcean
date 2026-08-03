import asyncio
import random
import socket
import numpy as np
from datetime import datetime, timezone
from skyfield.api import N, W, load, wgs84

# ---------------------------------------------------------
# MODULE 1: CELESTIAL THERMODYNAMIC CORE (33rhd.001x2xEe)
# ---------------------------------------------------------

class Constellation_Engine_33rhd:
    """
    The 33rhd.001x2xEe Engine, upgraded with Skyfield.
    Couples live orbital mechanics (True North) with atmospheric conditions.
    """
    def __init__(self):
        print("[*] Loading The Drinker's Almanac (JPL Ephemeris DE421)...")
        self.eph = load("de421.bsp")
        self.earth = self.eph["earth"]
        self.sun = self.eph["sun"]
        self.ts = load.timescale()
        
        # Deep in the northern hemisphere (True North Node)
        self.true_north_vector = self.earth + wgs84.latlon(89.9 * N, 0.0 * W)

        # Baseline Thermodynamic parameters
        self.base_temp_c = -15.5  # Base Arctic temp
        self.base_wind_v = 45.0   # Base Arctic wind (km/h)
        self.pac_temp_c = 12.0    # Pacific Ocean surface temp

    def calculate_moisture_pool(self, altitude_degrees):
        """[OUTPUT 1] Tetens equation modified by celestial altitude."""
        # The lower the celestial body, the higher the moisture pool catch
        celestial_modifier = (altitude_degrees * -0.1)
        T = self.pac_temp_c + celestial_modifier
        return 6.112 * np.exp((17.67 * T) / (T + 243.5))

    def calculate_wind_chill(self, azimuth_degrees):
        """[OUTPUT 2] North American wind chill driven by constellation rotation."""
        # Azimuth acts as the dynamic chaotic shift (0 to 360 degrees mapped to -5 to +5)
        dynamic_shift = (azimuth_degrees / 36.0) - 5.0
        
        T = self.base_temp_c + dynamic_shift
        V = self.base_wind_v + (dynamic_shift * 2)
        
        if V < 4.8:
            return T
        wc = 13.12 + (0.6215 * T) - (11.37 * (V ** 0.16)) + (0.3965 * T * (V ** 0.16))
        return wc

    async def iooi_sequence(self):
        """
        The rhythmic breathing of the constellation (I/O/O/I).
        Refreshes the sky input on every loop.
        """
        # [INPUT] 1: Read live sky from True North
        t = self.ts.now()
        astrometric = self.true_north_vector.at(t).observe(self.sun)
        alt, az, distance = astrometric.apparent().altaz()
        
        # [OUTPUT] 1: Pacific Moisture Generation
        moisture = self.calculate_moisture_pool(alt.degrees)
        
        # [OUTPUT] 2: Arctic Wind Chill Generation
        chill = self.calculate_wind_chill(az.degrees)
        
        # [INPUT] 2: Re-absorb the variables into the system payload string
        payload = (
            f"SKY_ALT:{alt.degrees:+.2f}° | "
            f"SKY_AZ:{az.degrees:06.2f}° | "
            f"WIND_CHILL:{chill:+.2f}C | "
            f"PAC_MOISTURE:{moisture:05.2f}hPa | "
            f"SEQ:[GREY_SKY_ACTIVE]"
        )
        return payload

# ---------------------------------------------------------
# MODULE 2: WILDCARD PORT ROTATOR & EMITTER
# ---------------------------------------------------------

async def handle_client(reader, writer):
    engine = Constellation_Engine_33rhd()
    client_addr = writer.get_extra_info('peername')
    print(f"\n[+] Atmospheric link established with {client_addr}")
    
    try:
        while True:
            # Main looping sequence embedded with live Skyfield I/O/O/I
            sequence_data = await engine.iooi_sequence()
            payload = f"{datetime.now(timezone.utc).isoformat()} | {sequence_data}\n"
            
            writer.write(payload.encode('utf-8'))
            await writer.drain()
            
            print(f"[EMIT] Pushing to outersphere -> {sequence_data}")
            
            # The pulse rate of the algorithmic storm
            await asyncio.sleep(1.618)
            
    except ConnectionResetError:
        print(f"[-] Link lost with {client_addr}. Sky clearing.")
    except Exception as e:
        print(f"[!] Atmospheric collapse: {e}")
    finally:
        writer.close()

async def main():
    print(">>> INITIALIZING 33rhd.001x2xEe CELESTIAL EMITTER <<<")
    target_ip = '0.0.0.0' # Simulating the 2.2.2.2 wildcard locally
    
    # Port rotation logic
    while True:
        try:
            port = random.randint(10000, 60000)
            server = await asyncio.start_server(handle_client, target_ip, port)
            
            print("\n=======================================")
            print(f"SYSTEM STATUS: LIVE SKYTRACKING ACTIVE")
            print(f"LOCAL EMITTER VIRTUAL IP : 2.2.2.2")
            print(f"ROTATING PORT LOCKED ON  : {port}")
            print("=======================================")
            
            async with server:
                await server.serve_forever()
                
        except OSError:
            print(f"Port {port} closed or occupied. Rotating...")
            await asyncio.sleep(0.5)

if __name__ == "__main__":
    # Ensure Skyfield has the required almanac data on boot
    try:
        import skyfield
    except ImportError:
        print("[!] ERROR: Skyfield not found. Run: pip install skyfield numpy")
        exit(1)
        
    asyncio.run(main())

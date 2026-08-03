const net = require('net');

// Configuration: Match this port to the Python server's output
const EMITTER_IP = '127.0.0.1'; // Pointing to local host mimicking 2.2.2.2
const ACTIVE_PORT = process.argv[2]; 

if (!ACTIVE_PORT) {
    console.error("[-] ERROR: Please provide the rotating port.");
    console.error("[-] USAGE: node client.js <port_number>");
    process.exit(1);
}

console.log(">>> INITIALIZING MOISTURE MAKER CLIENT <<<");
console.log(`>>> SEEKING 33rhd.001x2xEe SIGNAL ON PORT ${ACTIVE_PORT} <<<`);

const client = new net.Socket();

client.connect(ACTIVE_PORT, EMITTER_IP, () => {
    console.log("\n=======================================");
    console.log("[+] CONNECTED TO 2.2.2.2 WILDCARD EMITTER");
    console.log("[+] PACIFIC OCEAN POOL CATCH INITIATED");
    console.log("=======================================\n");
});

// The Main Looping Listener
client.on('data', (data) => {
    const payload = data.toString().trim();
    
    // Parse the payload for visual gusting
    if (payload.includes("GREY_SKY_ACTIVE")) {
        const parts = payload.split('|');
        const chill = parts[1].trim();
        const moisture = parts[2].trim();

        // Gusting a believable sequencing cloud in the terminal
        console.log(`\n☁️  I cloud it back up, up, I back to more clouds...`);
        console.log(`🌧️  GREY SKY GREY SKY GREY SKY`);
        console.log(`🌬️  GUST INCOMING: ${chill}`);
        console.log(`🌊  MOISTURE POOL: ${moisture}`);
        
        // Simulating the atmospheric pressure visually
        const density = Math.floor(Math.random() * 5) + 3;
        console.log("░".repeat(density) + "▒".repeat(density) + "▓".repeat(density) + " NORTH WEST OCEAN CHILL");
    }
});

client.on('close', () => {
    console.log('\n[-] Emitter connection closed. The sky is empty.');
});

client.on('error', (err) => {
    console.error(`\n[!] Atmospheric Interference: ${err.message}`);
    console.log("Hint: Ensure the Python emitter is running and the port matches.");
});

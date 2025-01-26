#!/usr/bin/env python3

import os
import random
import subprocess

# List of server files
server_files = [
    "/path/to/server1.ovpn",
    "/path/to/server2.ovpn",
    "/path/to/server3.ovpn"
]

# Credentials
SUDO_PASSWORD = "A1qs2wd3e@"
VPN_USERNAME = "vpnbook"
VPN_PASSWORD = "your_vpnbook_password"

def automate_openvpn():
    # Randomly select a server file
    server_file = random.choice(server_files)
    print(f"Selected server file: {server_file}")

    # OpenVPN command
    openvpn_command = f"sudo -S openvpn --config {server_file}"

    # Run the OpenVPN command with subprocess
    process = subprocess.Popen(
        openvpn_command.split(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        # Pass the sudo password
        process.stdin.write(f"{SUDO_PASSWORD}\n")
        process.stdin.flush()

        # Pass the VPN username and password when prompted
        while True:
            output = process.stdout.readline()
            print(output, end="")  # Print the output to monitor progress
            if "Enter Auth Username" in output:
                process.stdin.write(f"{VPN_USERNAME}\n")
                process.stdin.flush()
            elif "Enter Auth Password" in output:
                process.stdin.write(f"{VPN_PASSWORD}\n")
                process.stdin.flush()

            # Break the loop if the process ends
            if process.poll() is not None:
                break

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        process.stdin.close()
        process.stdout.close()
        process.stderr.close()

if __name__ == "__main__":
    automate_openvpn()

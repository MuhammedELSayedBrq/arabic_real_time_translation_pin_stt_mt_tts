import subprocess

def get_connected_devices():
    """
    Uses `arp -a` to scan your network and return a list of connected devices,
    handling potential index errors and providing informative error messages.

    Returns:
        list: A list of dictionaries containing details of connected devices:
              [{'ip': '192.168.1.2', 'mac': '00:11:22:33:44:55', 'device_name': 'unknown'}, ...]
    """

    try:
        output = subprocess.check_output(["arp", "-a"]).decode("utf-8")
        lines = output.splitlines()

        # Skip header and empty lines
        devices = []
        for line in lines[2:]:
            if not line:
                continue

            parts = line.split()

            try:
                # Handle potential index errors:
                ip = parts[0]
                mac = parts[3]
                device_name = " ".join(parts[4:]) if len(parts) > 4 else "unknown"

            except IndexError:
                #print(f"Warning: Unexpected ARP output format on line: {line}")
                devices.append(line)

        return devices

    except subprocess.CalledProcessError as e:
        print(f"Error running `arp -a`: {e}")
        return []  # Return an empty list on error

def get_ip():
    connected_devices = get_connected_devices()
    raspberry = []
    for device in connected_devices:
        devices = device.split(" ")
        #print(devices)
        for index, item in enumerate(devices):
            if item == "28-cd-c1-0e-7b-55":
                raspberry.append(device)
    ip_first = raspberry[0]
    ip = ip_first.strip().split()[0]
    return ip
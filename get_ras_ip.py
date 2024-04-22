import subprocess

def get_connected_devices():
    try:
        output = subprocess.check_output(["arp", "-a"]).decode("utf-8")
        lines = output.splitlines()

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
                devices.append(line)

        return devices

    except subprocess.CalledProcessError as e:
        print(f"Error running `arp -a`: {e}")
        return []

def get_ip():
    connected_devices = get_connected_devices()
    raspberry = []
    for device in connected_devices:
        devices = device.split(" ")
        #print(devices)
        for item in devices:
            if item == "28-cd-c1-0e-7b-55":
                raspberry.append(device)

    ip_first = raspberry[0]
    ip = ip_first.strip().split()[0]

    return ip

if __name__ == '__main__':
    print(get_ip())
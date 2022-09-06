"""
Ubuntu 20.04 might not always do a good job of picking audio devices as they are plugged in/out (bluetooth headset,
external speakers/mic conected through a docking station, etc). So this script can automate the selection based on the
rules configuration up above (list of preferred output/input devices in order).

This script can be scheduled to run as a cron every X minutes so that switching is done as fast as possible.

#TODO find a way to trigger the script on device change instead of cron scheduling
"""
import os
import subprocess, re

output_devices = [
    'Pixel USB-C earbuds Analog Stereo',
    'Bose QuietComfort 35',
    'Razer Hammerhead True Wireless Earbuds',
    'USB Audio Line Out',
    'Built-in Audio Analog Stereo'
]

input_devices = [
    'Pixel USB-C earbuds Mono',
    'Yeti Nano Analog Stereo',
    'Built-in Audio Analog Stereo'
]

def setDefaultDevice(type, preferrence_list):
    if( type != 'sink' and type != 'source'):
        print("Invalid device type")
        exit(-1)
    result = subprocess.run([f'pacmd', f'list-{type}s'], stdout=subprocess.PIPE)
    stdout = result.stdout.decode('utf-8')
    device_list = []
    device_index = []
    index = 0
    for line in stdout.splitlines():
        clean_line = line.lstrip().replace('* ','')
        if clean_line.startswith('index: '):
            index = clean_line.replace('index: ', '')
        if clean_line.startswith('device.description'):
            match = re.search('"(.*)"', line)
            device_list.append(match.group(1))
            device_index.append(int(index))
        # End if
    # End for

    for preferred_device in preferrence_list:
        try:
            ary_idx = device_list.index(preferred_device)
            index = device_index[ary_idx]
            if index >= 0:
                print(f'Setting {type} to {preferred_device}')
                cmd = f'pacmd set-default-{type} {index}'
                print(f'cmd is: {cmd}')
                os.system(cmd)
                break
        except:
            # Do nothing - device_list.index() probably threw a ValueError because something wasn't found
            continue
    return

if __name__ == '__main__':
    # Update output devices
    setDefaultDevice('sink', output_devices)

    # Update input devices
    setDefaultDevice('source', input_devices)

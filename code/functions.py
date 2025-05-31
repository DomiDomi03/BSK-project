##
#	@file functions.py
#	@details File to store static functions used in whole project
#	@date 10-04-2025
##

import psutil

## Static function that scans all mounted disk partitions on the system and returns a set of device paths.
# @return list of available devices
@staticmethod
def find_devices():
    return {p.device for p in psutil.disk_partitions()}

## Static function returns a set of device paths for all mounted removable drives, such as USB flash drives or other removable storage devices.
# @return list of available removable devices
@staticmethod
def find_usb():
    return {p.device for p in psutil.disk_partitions() if 'removable' in p.opts.lower()}

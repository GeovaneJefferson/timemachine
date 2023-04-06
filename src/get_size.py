from setup import *
from read_ini_file import UPDATEINIFILE


def get_disk_max_size():
    mainIniFile = UPDATEINIFILE()

    # Get external max size
    externalMaxSize = os.popen(f"df --output=size -h {str(mainIniFile.ini_external_location())}")
    externalMaxSize = externalMaxSize.read().strip().replace("1K-blocks", "").replace(
        "Size", "").replace("\n", "").replace(" ", "")
    return str(externalMaxSize)

def get_disk_used_size():
    mainIniFile = UPDATEINIFILE()

    # Get external usded size
    usedSpace = os.popen(f"df --output=used -h {str(mainIniFile.ini_external_location())}")
    usedSpace = usedSpace.read().strip().replace("1K-blocks", "").replace(
        "Used", "").replace("\n", "").replace(" ", "")

    return str(usedSpace)

def get_available_devices_size(device):
    # Get external max size
    externalMaxSize = os.popen(f"df --output=size -h {device}")
    externalMaxSize = externalMaxSize.read().strip().replace("1K-blocks", "").replace(
        "Size", "").replace("\n", "").replace(" ", "")

    # Get external usded size
    usedSpace = os.popen(f"df --output=used -h {device}")
    usedSpace = usedSpace.read().strip().replace("1K-blocks", "").replace(
        "Used", "").replace("\n", "").replace(" ", "")

    return usedSpace+"/"+externalMaxSize

if __name__ == '__main__':
    pass
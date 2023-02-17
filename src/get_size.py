from setup import *
config = configparser.ConfigParser()
config.read(src_user_config)
iniExternalLocation = config['EXTERNAL']['hd']

def get_disk_max_size():
    # Get external max size
    externalMaxSize = os.popen(f"df --output=size -h {iniExternalLocation}")
    externalMaxSize = externalMaxSize.read().strip().replace("1K-blocks", "").replace(
        "Size", "").replace("\n", "").replace(" ", "")
    return str(externalMaxSize)

def get_disk_used_size():
    # Get external usded size
    usedSpace = os.popen(f"df --output=used -h {iniExternalLocation}")
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

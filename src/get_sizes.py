from setup import *
from read_ini_file import UPDATEINIFILE
from device_location import device_location


MAIN_INI_FILE = UPDATEINIFILE()

def get_external_device_max_size():
    # Get external max size
    external_max_size = os.popen(
        f"df --output=size -h {MAIN_INI_FILE.hd_hd()}")
    external_max_size = external_max_size.read().strip()\
                            .replace("1K-blocks", "")\
                            .replace("Size", "")\
                            .replace("\n", "")\
                            .replace(" ", "")
    
    return str(external_max_size)

def get_external_device_used_size():
    used_space = os.popen(
        f"df --output=avail -h {MAIN_INI_FILE.hd_hd()}").read().strip()\
                            .replace("1K-blocks", "")\
                            .replace("Avail", "")\
                            .replace("\n", "")\
                            .replace(" ", "")

    return str(used_space)

def get_external_device_free_size():
    try:
        # External free space
        available_device_space = os.popen(
            f"df --output=avail -B1 {MAIN_INI_FILE.hd_hd()}")
        available_device_space = available_device_space.read().strip()\
            .replace("1K-blocks", "")\
            .replace("Avail", "")\
            .replace("\n", "")\
            .replace(" ", "")
        
        return int(available_device_space)
    
    except ValueError:
        print("Device is probably not connected.")
        exit()

def get_external_device_string_size(device):
    # Get external max size
    external_max_size=os.popen(
        f"df --output=size -h {device}").read().strip().replace(
        "1K-blocks", "").replace(
        "Size", "").replace(
        "\n", "").replace(
        " ", "")

    # Get external usded size
    used_space = os.popen(f"df --output=used -h {device}")
    used_space = used_space.read().strip().replace("1K-blocks", "").replace(
        "Used", "").replace("\n", "").replace(" ", "")

    return used_space + "/" + external_max_size

def get_all_used_backup_device_space(device):
    # If inside /Media
    if device_location():
        used_space = os.popen(
            f"df --output=avail -h {MEDIA}/{USERNAME}/{device}").read().\
            strip().replace(
            "1K-blocks", "").replace(
            "Avail", "").replace(
            "\n", "").replace(
            " ", "")

    # If inside /Run
    else:
        used_space = os.popen(f"df --output=avail -h {RUN}/{USERNAME}/{device}").read().\
            strip().replace(
            "1K-blocks", "").replace(
            "Avail", "").replace(
            "\n", "").replace(
            " ", "")

    return str(used_space)

def get_all_max_backup_device_space(device):
    # If inside /Media
    if device_location():
        external_max_size=os.popen(f"df --output=size -h {MEDIA}/{USERNAME}/{device}").read().strip().replace(
            "1K-blocks", "").replace(
            "Size", "").replace(
            "\n", "").replace(
            " ", "")
    
    # If inside /Run
    else:
        external_max_size=os.popen(f"df --output=size -h {RUN}/{USERNAME}/{device}").read().strip().replace(
            "1K-blocks", "").replace(
            "Size", "").replace(
            "\n", "").replace(
            " ", "")
    
    return str(external_max_size)

def needeed_size_to_backup_home():
    global lines

    # Read the file and initialize a total size variable
    total_size = 0

    # Read each line from the input file
    with open(MAIN_INI_FILE.include_to_backup(), "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):
            try:
                size_line = lines[i + 1]
                size = int(size_line.split()[1])  # Extract the size (convert to int)
                total_size += size
            
            except ValueError:
                total_size += 0
            except IndexError:
                pass

    # Conver to GB
    # gb_value = total_size / 1024**3

    # print()
    # print(f"Total size of all items: {total_size} bytes")
    # print(f"Total size of all items: {gb_value:.2f} GB")

    return int(total_size)
   
def number_of_item_to_backup():
    # Grab "lines" value
    needeed_size_to_backup_home()

    try:
        # Num. of item to be backed up
        num_of_item = round(len(lines) / 5)

        print(f"Num. of itens to backup: {num_of_item}")

        return num_of_item

    except:
        return 0

def get_directory_size(directory):
    total_size = 0

    # Function to recursively calculate total size of a directory
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    
    return total_size

def get_item_size(item_path):
    item_size = 0

    # Add the new item to date, and time folders
    if os.path.isdir(item_path):
        item_size = get_directory_size(item_path)

    elif os.path.isfile(item_path):
        item_size = os.path.getsize(item_path)
  
    try:
        return item_size
    except UnboundLocalError:
        return 0


if __name__ == '__main__':
    pass
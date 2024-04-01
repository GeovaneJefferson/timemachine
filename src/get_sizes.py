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
        f'df --output=avail -h {MAIN_INI_FILE.hd_hd()}').read().strip()\
                .replace('1K-blocks', '')\
                .replace('Avail', '')\
                .replace('\n', '')\
                .replace(' ', '')
    
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
    # MEDIA
    if device_location():
        used_space = os.popen(
            f"df --output=avail -h {MAIN_INI_FILE.hd_hd()}").read().\
            strip().replace(
            "1K-blocks", "").replace(
            "Avail", "").replace(
            "\n", "").replace(
            " ", "")
    else:
        # RUN
        used_space = os.popen(f"df --output=avail -h {RUN}/{USERNAME}/{device}").read().\
            strip().replace(
            "1K-blocks", "").replace(
            "Avail", "").replace(
            "\n", "").replace(
            " ", "")

    return str(used_space)

def get_used_backup_space():
    x = get_all_max_backup_device_space()
    y = get_external_device_used_size()
    value = []

    # Filter max space
    filter1 = []
    for i in x:
        if i.isdigit():
            filter1.append(i)
        else:
            # Add str to value
            value.append(i)

    # Filter total devices space
    total_device_space = int(''.join(filter1))
    
    # Filter used space
    filter2 = []
    for i in y:
        if i.isdigit():
            filter2.append(i)

    # Filter used device space
    used_device_space = int(''.join(filter2))
    
    value = ''.join(value)
    result = total_device_space - used_device_space
    return str(result) + value

def get_all_max_backup_device_space():
    external_max_size=os.popen(f"df --output=size -h {MAIN_INI_FILE.hd_hd()}").read().strip().replace(
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
        for i in range(1, len(lines), 5):
            try:
                size = int(lines[i].split()[1])  # Extract the size (convert to int)
                total_size += size
            except (ValueError, IndexError):
                pass

    # Conver to GB
    gb_value = total_size / 1024**3

    print()
    print(f"Total size of all items: {total_size} bytes")
    print(f"Total size of all items: {gb_value:.2f} GB")

    return int(total_size)
   
def number_of_item_to_backup():
    # Grab "lines" value
    needeed_size_to_backup_home()

    try:
        count_filename = 0
        count_new_file = 0
        count_updated_file = 0
        with open(MAIN_INI_FILE.include_to_backup(), "r") as f:
            for line in f:
                # Assuming each entry starts with "Filename:"
                if line.startswith("Filename:"):
                    count_filename += 1

                # New file count
                if line.startswith("Status: NEW"):
                    count_new_file += 1

                # Updated file count
                if line.startswith("Status: UPDATED"):
                    count_updated_file += 1

        print(f'Total items to be backup: {count_filename}')
        print(f'NEW Items: {count_new_file}')
        print(f'UPDATED Items: {count_updated_file}')
        return count_filename
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
        # In bytes
        return item_size
    except UnboundLocalError:
        return 0


if __name__ == '__main__':
    print(get_all_max_backup_device_space())
    pass

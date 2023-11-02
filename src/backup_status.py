from setup import *
from read_ini_file import UPDATEINIFILE
from get_sizes import get_item_size


MAIN_INI_FILE = UPDATEINIFILE()
base_storage_size = int()
list_of_zeros  = []

def backup_status(item_minus, item_sum_size, total_items):
    percentage = (item_minus / total_items) * 100

    # Source of backup folder size
    external_device_size = get_item_size(MAIN_INI_FILE.backup_dates_location())

    # Base storage size = Current total backup size needeed + external backup folder size
    # 2 GB + 12 GB = 14 GB
    after_backup_size = item_sum_size + external_device_size

    # Base storage size - current external backup folder size
    size_left_to_backup = after_backup_size - external_device_size
   
    # Convert item size to GB
    converted_size = size_left_to_backup / 1000**3
    
    print(f'{external_device_size / 1000**3:.1f} GB')
    print(f'{after_backup_size / 1000**3:.1f}' )
    print(f'{size_left_to_backup / 1000**3}')

    return str(f'{percentage:.1f}% done - {converted_size:.2f} GB left to be copied.') 


if __name__ == '__main__':

    # print(MAIN_INI_FILE.backup_dates_location())
    

    # # Count how many int has in
    # number_of_zeros = len(str(external_device_size)) - 2 

    # # Loop through zeros
    # for i in range(number_of_zeros):
    #     list_of_zeros.append('0')

    # # Add all necessery 0
    # number_of_zeros = str('1') + ''.join(list_of_zeros) 
    
    # # External 'backups' folder GB size
    # result_string = f'{external_device_size / int(number_of_zeros):.1f}'

    # print(result_string)



    # 14 GB - 1 GB = 1 GB left to be backup
    
    pass
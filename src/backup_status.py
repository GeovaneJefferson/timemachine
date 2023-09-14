from setup import *
from read_ini_file import UPDATEINIFILE
from get_sizes import number_of_item_to_backup


total_items = number_of_item_to_backup()
# total_items = 22

def backup_status(item_minus, item_sum_size):
    item_lenght = total_items - item_minus

    percentage = (item_lenght / total_items) * 100
    # Convert item size to GB
    item_sum_size = item_sum_size / 1024**3

    print(f'{(percentage):.1f}% done - {item_sum_size:.2f} GB copied')
    return f'{(percentage):.1f}% done - {item_sum_size:.2f} GB copied' 


if __name__ == '__main__':
    pass
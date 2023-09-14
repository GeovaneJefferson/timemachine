from setup import *


def backup_status(item_minus, item_sum_size, total_items):
    percentage = (item_minus / total_items) * 100

    # Convert item size to GB
    item_sum_size = item_sum_size / 1024**3

    print(f'{(percentage):.1f}% done - {item_sum_size:.2f} GB copied')
    return str(f'{(percentage):.1f}% done - {item_sum_size:.2f} GB copied') 


if __name__ == '__main__':
    pass
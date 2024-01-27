from setup import *


def create_directory(location):
    # Is a directory to a file
    if '.' in str(location).split('/')[-1]:
        # Extract the directory path from the file path
        directory = os.path.dirname(location)

    else:
        # Extract the directory path from the file path
        directory = location

    # Check if the directory exists, and create it if necessary
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist. Creating...")
        try:
            os.makedirs(directory)
            print(f"Directory '{directory}' created successfully.")
        except Exception as e:
            print(f"Error creating directory: {e}")

def create_file(location):
    # Check if the file already exists
    if not os.path.exists(location):
        print('File does not exist. Creating...')
        
        # Create the file
        try:
            with open(location, 'w'):
                pass  # This creates an empty file
            print('File created successfully.')
        except Exception as e:
            print(f"Error creating file: {e}")
    else:
        print('File already exists.')


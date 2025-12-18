import pystray
from PIL import Image
import os
import threading

# --- 1. SIMULATED DATA ---
MAX_DISPLAY_ITEMS = 5

PENDING_CHANGES = [
    ("Modified", "/home/user/documents/report_q4.docx"),
    ("Deleted", "/home/user/images/old_vacation_plan.pdf"),
    ("Modified", "/home/user/code/daemon.py"),
    ("Modified", "/home/user/code/app.py"),    
    ("Modified", "/home/user/temp/data_log_1.txt"), 
    ("Deleted", "/home/user/backup/backup_config.json"),
]

# --- 2. MENU ACTION HANDLER ---
def handle_file_action(icon, action_type, file_path):
    """Function executed when a file item is clicked."""
    print(f"File action requested: '{action_type}' on '{file_path}'")
    
    global PENDING_CHANGES
    # Remove the clicked item
    PENDING_CHANGES = [item for item in PENDING_CHANGES if item != (action_type, file_path)]
    
    # Schedule menu update on the main thread
    icon.update_menu()

# --- 3. DYNAMIC MENU GENERATOR FUNCTION ---
def create_dynamic_file_menu(icon=None, item=None):
    """Dynamically generates the menu structure based on PENDING_CHANGES."""
    menu_items = []
    count = len(PENDING_CHANGES)
    
    if count > 0:
        # 1. Status Item
        menu_items.append(pystray.MenuItem(f"⚠️ {count} Files Need Review", None, enabled=False))
        menu_items.append(pystray.Menu.SEPARATOR)

        # 2. File List (limited to MAX_DISPLAY_ITEMS)
        for action, path in PENDING_CHANGES[:MAX_DISPLAY_ITEMS]:
            filename = os.path.basename(path)
            display_text = f"[{action[0]}] {filename}"
            
            # Use lambda with default arguments to capture current values
            menu_items.append(pystray.MenuItem(
                display_text, 
                lambda _, act=action, p=path: handle_file_action(icon, act, p)
            ))

        # 3. 'View All' Item for overflow
        if count > MAX_DISPLAY_ITEMS:
            overflow_count = count - MAX_DISPLAY_ITEMS
            menu_items.append(pystray.MenuItem(
                f"...and {overflow_count} more (View All)", 
                lambda _: print("Opening full changes list in app...")
            ))
            
        menu_items.append(pystray.Menu.SEPARATOR)

    else:
        # Clear Status
        menu_items.append(pystray.MenuItem("✅ All Files Backed Up", None, enabled=False))
        menu_items.append(pystray.Menu.SEPARATOR)

    # 4. Standard Application Controls
    menu_items.append(pystray.MenuItem('Open App', lambda _: print("Launching UI..."), default=True))
    menu_items.append(pystray.MenuItem('Exit App', lambda i: i.stop()))
    
    return tuple(menu_items)

# --- 4. MAIN APPLICATION ---
def setup_icon():
    # Create a simple 64x64 icon if icon.png doesn't exist
    if not os.path.exists("icon.png"):
        img = Image.new('RGBA', (64, 64), (50, 100, 200, 255))
        img.save("icon.png")
    
    icon_image = Image.open("icon.png")
    
    icon = pystray.Icon(
        "my_app",
        icon_image,
        "My Backup App",
        menu=pystray.Menu(lambda: create_dynamic_file_menu(icon))
    )
    
    return icon

# Run the application
if __name__ == "__main__":
    icon = setup_icon()
    
    # Optional: Simulate dynamic updates
    def simulate_changes():
        import time
        time.sleep(5)
        
        # Add a new item after 5 seconds
        global PENDING_CHANGES
        PENDING_CHANGES.append(("Modified", "/home/user/new_file.txt"))
        print("Added new file, updating menu...")
        icon.update_menu()
        
        # Remove all items after another 5 seconds
        time.sleep(5)
        PENDING_CHANGES.clear()
        print("Cleared all files, updating menu...")
        icon.update_menu()
    
    # Start simulation in a separate thread
    thread = threading.Thread(target=simulate_changes, daemon=True)
    thread.start()
    
    # This call will start the application and is blocking
    icon.run()
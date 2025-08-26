from server import *  # Assuming server.py is in the same directory or accessible

server = SERVER()

# Define file categories and their extensions (consistent with ui.py)
FILE_CATEGORIES = {
    "Image": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff", ".ico"},
    "Video": {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".wmv"},
    "Document": {".pdf", ".doc", ".docx", ".odt", ".xls", ".xlsx", ".ods", ".ppt", ".pptx", ".odp", ".txt", ".md", ".rtf", ".csv"},
    # Add other categories as needed, e.g., Audio, Archive
}

def _format_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def _get_file_category(filename):
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"

def generate_summary():
    # logging.info("Generating backup summary...")
    backup_root = server.backup_folder_name()
    summary_output_path: str = server.get_summary_filename()

    category_stats = {
        "Image": {"count": 0, "size": 0},
        "Video": {"count": 0, "size": 0},
        "Document": {"count": 0, "size": 0},
        "Others": {"count": 0, "size": 0},
    }

    # --- Calculate Category Stats from Main Backup ---
    main_backup_path = server.main_backup_folder()
    if not os.path.exists(main_backup_path):
        logging.warning(f"Main backup path {main_backup_path} not found. Cannot generate summary.")
        # Save an empty or default summary
        with open(summary_output_path, 'w') as f:
            json.dump({"categories": [], "most_frequent_backups": [], "error": "Backup path not found"}, f, indent=4)
        return

    logging.info(f"Starting walk in main backup path: {main_backup_path} for category stats.")
    files_processed_count = 0
    try:
        for root, dirs, files_in_dir in os.walk(main_backup_path):
            logging.debug(f"Summary (main): Walking directory: {root}")
            # Exclude hidden directories from further traversal
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for filename in files_in_dir:
                if filename.startswith('.'): # Skip hidden files
                    continue
                
                file_path = os.path.join(root, filename)
                try:
                    if os.path.isfile(file_path) and not os.path.islink(file_path):
                        category = _get_file_category(filename)
                        category_stats[category]["count"] += 1
                        category_stats[category]["size"] += os.path.getsize(file_path)
                        files_processed_count += 1
                        # if files_processed_count % 2000 == 0: # Log progress
                        #     logging.info(f"Processed {files_processed_count} files for main backup summary (current: {file_path})...")
                except FileNotFoundError:
                    logging.warning(f"File not found during summary generation (main): {file_path}")
                    continue
                except Exception as e:
                    logging.error(f"Error processing file {file_path} for summary (main): {e}")
                    continue
    except Exception as e_walk:
        logging.error(f"[CRITICAL]: Error during os.walk in {main_backup_path} for summary: {e_walk}", exc_info=True)
        with open(summary_output_path, 'w') as f:
            json.dump({"categories": [], "most_frequent_backups": [], "most_frequent_recent_backups": [], "error": f"Error during summary generation: {e_walk}"}, f, indent=4)
        raise # Re-raise to ensure the calling process (daemon) knows it failed
    # logging.info(f"Finished walk in {main_backup_path} for category stats. Total files processed: {files_processed_count}")

    # --- Calculate Most Frequent Backups from Incremental Backups ---
    file_backup_counts = {}
    recent_file_backup_counts = {} # For files backed up in the last 5 days
    five_days_ago = datetime.now() - timedelta(days=5)
    main_backup_folder_name = os.path.basename(main_backup_path)

    if os.path.exists(backup_root):
        # logging.info(f"Starting walk in incremental backup root: {backup_root} for frequency stats.")
        incremental_files_processed_count = 0
        for date_folder_name in os.listdir(backup_root):
            date_folder_path = os.path.join(backup_root, date_folder_name)

            # Skip the main backup folder and any non-directory entries
            if date_folder_name == main_backup_folder_name or not os.path.isdir(date_folder_path):
                continue

            is_recent_date = False
            try:
                backup_date = datetime.strptime(date_folder_name, "%d-%m-%Y")
                if backup_date >= five_days_ago:
                    is_recent_date = True
            except ValueError:
                logging.warning(f"Skipping invalid date folder format: {date_folder_name}")
                continue

            for time_folder_name in os.listdir(date_folder_path):
                time_folder_path = os.path.join(date_folder_path, time_folder_name)

                # Skip non-directory entries
                if not os.path.isdir(time_folder_path):
                    continue

                logging.debug(f"Summary (incremental): Walking directory: {time_folder_path}")
                # Walk through the files in this specific time-stamped backup
                for root_inc, _, files_inc in os.walk(time_folder_path):
                    # Calculate the relative path from the time_folder_path
                    rel_root_from_time_folder = os.path.relpath(root_inc, time_folder_path)

                    for filename_loop in files_inc: # Renamed to avoid conflict
                        original_rel_path = os.path.join(rel_root_from_time_folder, filename_loop)
                        original_rel_path = original_rel_path.replace("\\", "/") # Normalize path separators
                        file_backup_counts[original_rel_path] = file_backup_counts.get(original_rel_path, 0) + 1
                        if is_recent_date:
                            recent_file_backup_counts[original_rel_path] = recent_file_backup_counts.get(original_rel_path, 0) + 1
                        
                        incremental_files_processed_count +=1
                        # if incremental_files_processed_count % 2000 == 0: # Log progress
                        #     logging.info(f"Processed {incremental_files_processed_count} files for incremental summary (current: {os.path.join(root_inc, filename_loop)})...")
        # logging.info(f"Finished walk in {backup_root} for incremental backup stats. Total files processed: {incremental_files_processed_count}")


    # Sort files by backup count in descending order and select top N
    sorted_files = sorted(file_backup_counts.items(), key=lambda item: item[1], reverse=True)
    sorted_recent_files = sorted(recent_file_backup_counts.items(), key=lambda item: item[1], reverse=True)

    summary_data = []
    for cat_name, data in category_stats.items():
        summary_data.append(
            {"name": cat_name,
             "count": data["count"], 
             "size_bytes": data["size"], 
             "size_str": _format_size(data["size"])})

    top_n = 5
    most_frequent_backups = [{"path": path, "count": count} for path, count in sorted_files[:top_n]]
    most_frequent_recent_backups = [{"path": path, "count": count} for path, count in sorted_recent_files[:top_n]]

    # Prepare final summary data structure
    summary_output_data = {
        "categories": summary_data,
        "most_frequent_backups": most_frequent_backups,
        "most_frequent_recent_backups": most_frequent_recent_backups # Add new list
    }
    with open(summary_output_path, 'w') as f:
        json.dump(summary_output_data, f, indent=4)
    logging.info(f"Backup summary generated and saved to {summary_output_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    generate_summary()
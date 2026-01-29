"""
Backup Summary Generator for Time Machine Application

This module generates comprehensive backup summaries including:
- File category statistics (Images, Videos, Documents, Others)
- Most frequently backed up files
- Recent backup frequency analysis
"""

import os
import json
import math
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from server import SERVER 

# Initialize server instance
server = SERVER()

# File categories and their extensions (consistent with ui.py)
FILE_CATEGORIES = {
    "Image": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".tiff", ".ico"},
    "Video": {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".wmv"},
    "Document": {".pdf", ".doc", ".docx", ".odt", ".xls", ".xlsx", ".ods", 
                 ".ppt", ".pptx", ".odp", ".txt", ".md", ".rtf", ".csv"},
    # Add other categories as needed, e.g., Audio, Archive
}

# Configuration constants
TOP_N_FREQUENT_FILES = 5
RECENT_DAYS_THRESHOLD = 5
PROGRESS_LOG_INTERVAL = 2000  # Log progress every N files


def _format_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable string (e.g., "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_units = ("B", "KB", "MB", "GB", "TB")
    exponent = int(math.floor(math.log(size_bytes, 1024)))
    divisor = math.pow(1024, exponent)
    size_value = round(size_bytes / divisor, 2)
    
    return f"{size_value} {size_units[exponent]}"


def _get_file_category(filename: str) -> str:
    """
    Determine file category based on extension.
    
    Args:
        filename: Name of the file
        
    Returns:
        Category name ("Image", "Video", "Document", or "Others")
    """
    _, extension = os.path.splitext(filename)
    extension = extension.lower()
    
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    
    return "Others"


def _initialize_category_stats() -> Dict[str, Dict[str, int]]:
    """
    Initialize category statistics dictionary.
    
    Returns:
        Dictionary with initialized category statistics
    """
    return {
        category: {"count": 0, "size": 0}
        for category in list(FILE_CATEGORIES.keys()) + ["Others"]
    }


def _process_main_backup_files(main_backup_path: str) -> Dict[str, Dict[str, int]]:
    """
    Process files in main backup directory to collect category statistics.
    
    Args:
        main_backup_path: Path to main backup directory
        
    Returns:
        Dictionary containing category statistics
    """
    category_stats = _initialize_category_stats()
    files_processed = 0
    
    logging.info(f"Starting directory walk in main backup: {main_backup_path}")
    
    try:
        for root, dirs, files in os.walk(main_backup_path):
            logging.debug(f"Processing directory: {root}")
            
            # Exclude hidden directories from traversal
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for filename in files:
                # Skip hidden files
                if filename.startswith('.'):
                    continue
                
                file_path = os.path.join(root, filename)
                files_processed += _process_single_file(file_path, filename, category_stats)
                
                # # Log progress periodically
                # if files_processed % PROGRESS_LOG_INTERVAL == 0:
                #     logging.info(f"Processed {files_processed} files from main backup...")
                    
    except Exception as e:
        logging.error(f"Critical error during directory walk: {e}", exc_info=True)
        raise
    
    logging.info(f"Completed main backup processing. Total files: {files_processed}")
    return category_stats


def _process_single_file(file_path: str, filename: str, 
                        category_stats: Dict[str, Dict[str, int]]) -> int:
    """
    Process a single file and update category statistics.
    
    Args:
        file_path: Full path to the file
        filename: Name of the file
        category_stats: Category statistics dictionary to update
        
    Returns:
        1 if file was processed successfully, 0 otherwise
    """
    try:
        # Skip if not a regular file or is a symbolic link
        if not os.path.isfile(file_path) or os.path.islink(file_path):
            return 0
        
        # Get file category and size
        category = _get_file_category(filename)
        file_size = os.path.getsize(file_path)
        
        # Update category statistics
        category_stats[category]["count"] += 1
        category_stats[category]["size"] += file_size
        
        return 1
        
    except FileNotFoundError:
        logging.warning(f"File not found during processing: {file_path}")
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
    
    return 0


def _process_incremental_backups(backup_root: str, main_backup_folder_name: str
                               ) -> Tuple[Dict[str, int], Dict[str, int]]:
    """
    Process incremental backups to count file backup frequencies.
    
    Args:
        backup_root: Root backup directory
        main_backup_folder_name: Name of main backup folder to exclude
        
    Returns:
        Tuple of (all_time_counts, recent_counts) dictionaries
    """
    file_backup_counts = {}
    recent_file_backup_counts = {}
    
    if not os.path.exists(backup_root):
        logging.warning(f"Backup root directory not found: {backup_root}")
        return file_backup_counts, recent_file_backup_counts
    
    # Calculate date threshold for recent backups
    five_days_ago = datetime.now() - timedelta(days=RECENT_DAYS_THRESHOLD)
    files_processed = 0
    
    logging.info(f"Processing incremental backups from: {backup_root}")
    
    for date_folder_name in os.listdir(backup_root):
        date_folder_path = os.path.join(backup_root, date_folder_name)
        
        # Skip main backup folder and non-directories
        if (date_folder_name == main_backup_folder_name or 
            not os.path.isdir(date_folder_path)):
            continue
        
        # Check if this is a recent backup
        is_recent = _is_recent_backup_folder(date_folder_name, five_days_ago)
        
        # Process time-stamped backups within this date folder
        files_processed += _process_date_folder(
            date_folder_path, file_backup_counts, recent_file_backup_counts, is_recent
        )
    
    logging.info(f"Completed incremental backup processing. Total files: {files_processed}")
    return file_backup_counts, recent_file_backup_counts


def _is_recent_backup_folder(date_folder_name: str, threshold_date: datetime) -> bool:
    """
    Check if a backup folder is within the recent time threshold.
    
    Args:
        date_folder_name: Folder name in format "DD-MM-YYYY"
        threshold_date: Date threshold for recent backups
        
    Returns:
        True if backup is recent, False otherwise
    """
    try:
        backup_date = datetime.strptime(date_folder_name, "%d-%m-%Y")
        return backup_date >= threshold_date
    except ValueError:
        logging.warning(f"Skipping invalid date folder format: {date_folder_name}")
        return False


def _process_date_folder(date_folder_path: str, all_time_counts: Dict[str, int],
                        recent_counts: Dict[str, int], is_recent: bool) -> int:
    """
    Process all backup folders within a date folder.
    
    Args:
        date_folder_path: Path to date folder
        all_time_counts: Dictionary to update with all-time counts
        recent_counts: Dictionary to update with recent counts
        is_recent: Whether this date folder is considered recent
        
    Returns:
        Number of files processed in this date folder
    """
    files_processed = 0
    
    for time_folder_name in os.listdir(date_folder_path):
        time_folder_path = os.path.join(date_folder_path, time_folder_name)
        
        if not os.path.isdir(time_folder_path):
            continue
        
        logging.debug(f"Processing incremental backup: {time_folder_path}")
        
        # Walk through the time-stamped backup
        for root_inc, _, files_inc in os.walk(time_folder_path):
            # Calculate relative path from time folder
            rel_root = os.path.relpath(root_inc, time_folder_path)
            
            for filename in files_inc:
                original_rel_path = os.path.join(rel_root, filename)
                # Normalize path separators
                original_rel_path = original_rel_path.replace("\\", "/")
                
                # Update backup counts
                all_time_counts[original_rel_path] = all_time_counts.get(original_rel_path, 0) + 1
                if is_recent:
                    recent_counts[original_rel_path] = recent_counts.get(original_rel_path, 0) + 1
                
                files_processed += 1
                
                # Log progress periodically
                if files_processed % PROGRESS_LOG_INTERVAL == 0:
                    logging.info(f"Processed {files_processed} files from incremental backups...")
    
    return files_processed


def _prepare_summary_data(category_stats: Dict[str, Dict[str, int]],
                         all_time_counts: Dict[str, int], 
                         recent_counts: Dict[str, int]) -> Dict[str, Any]:
    """
    Prepare the final summary data structure.
    
    Args:
        category_stats: Category statistics
        all_time_counts: All-time file backup counts
        recent_counts: Recent file backup counts
        
    Returns:
        Complete summary data dictionary
    """
    # Prepare category summary
    categories_summary = []
    for category_name, data in category_stats.items():
        categories_summary.append({
            "name": category_name,
            "count": data["count"],
            "size_bytes": data["size"],
            "size_str": _format_size(data["size"])
        })
    
    # Get most frequent files
    sorted_all_time = sorted(all_time_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_recent = sorted(recent_counts.items(), key=lambda x: x[1], reverse=True)
    
    most_frequent_all_time = [
        {"path": path, "count": count} 
        for path, count in sorted_all_time[:TOP_N_FREQUENT_FILES]
    ]
    
    most_frequent_recent = [
        {"path": path, "count": count} 
        for path, count in sorted_recent[:TOP_N_FREQUENT_FILES]
    ]
    
    return {
        "categories": categories_summary,
        "most_frequent_backups": most_frequent_all_time,
        "most_frequent_recent_backups": most_frequent_recent,
        "generated_at": datetime.now().isoformat(),
        "summary_version": "1.0"
    }


def _save_error_summary(summary_path: str, error_message: str):
    """
    Save an error summary when normal processing fails.
    
    Args:
        summary_path: Path to save summary file
        error_message: Error description
    """
    error_data = {
        "categories": [],
        "most_frequent_backups": [],
        "most_frequent_recent_backups": [],
        "error": error_message,
        "generated_at": datetime.now().isoformat()
    }
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(error_data, f, indent=4)
    
    logging.error(f"Error summary saved: {error_message}")


def generate_summary():
    """
    Generate comprehensive backup summary including file categories and frequency analysis.
    
    This function:
    1. Processes main backup for category statistics
    2. Processes incremental backups for frequency analysis
    3. Generates and saves a JSON summary file
    """
    backup_root = server.app_backup_dir()
    app_root = server.devices_path() 
    summary_output_path = os.path.join(app_root, server.SUMMARY_FILENAME)
    
    logging.info("Starting backup summary generation...")
    
    # Check if main backup exists
    main_backup_path = server.app_main_backup_dir()
    if not os.path.exists(main_backup_path):
        logging.warning(f"Main backup path not found: {main_backup_path}")
        _save_error_summary(summary_output_path, "Backup path not found")
        return
    
    try:
        # Process main backup for category statistics
        category_stats = _process_main_backup_files(main_backup_path)
        
        # Process incremental backups for frequency analysis
        main_backup_folder_name = os.path.basename(main_backup_path)
        all_time_counts, recent_counts = _process_incremental_backups(
            backup_root, main_backup_folder_name
        )
        
        # Prepare and save final summary
        summary_data = _prepare_summary_data(category_stats, all_time_counts, recent_counts)
        
        with open(summary_output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=4)
        
        logging.info(f"Backup summary successfully generated: {summary_output_path}")
        
    except Exception as e:
        logging.error(f"Failed to generate backup summary: {e}", exc_info=True)
        _save_error_summary(summary_output_path, f"Summary generation failed: {str(e)}")
        raise  # Re-raise to notify calling process


if __name__ == "__main__":
    # Configure logging when run as standalone script
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
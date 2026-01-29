#!/usr/bin/env python3
"""
Inotify monitor utility - Check current inotify usage and limits on Linux.
Helps diagnose "too many watches" issues.

Usage:
  python3 py/inotify_monitor.py                  # Show current status
  python3 py/inotify_monitor.py --suggest-fix    # Show how to increase limits
"""
import os
import sys
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def get_inotify_limits():
    """Get current inotify limits and usage."""
    try:
        with open('/proc/sys/fs/inotify/max_user_instances', 'r') as f:
            max_instances = int(f.read().strip())
    except Exception:
        return None
    
    try:
        with open('/proc/sys/fs/inotify/max_user_watches', 'r') as f:
            max_watches = int(f.read().strip())
    except Exception:
        max_watches = None
    
    return {
        'max_instances': max_instances,
        'max_watches': max_watches,
    }


def get_inotify_usage():
    """Get current inotify usage for the current process."""
    try:
        pid = os.getpid()
        fd_dir = f'/proc/{pid}/fd'
        
        if not os.path.exists(fd_dir):
            return None
        
        # Count inotify file descriptors
        inotify_count = 0
        for fd in os.listdir(fd_dir):
            try:
                link = os.readlink(os.path.join(fd_dir, fd))
                if link.startswith('anon_inode:[inotify]'):
                    inotify_count += 1
            except Exception:
                pass
        
        return inotify_count
    except Exception:
        return None


def get_all_processes_inotify():
    """Get total inotify usage across all processes (if running as root)."""
    try:
        if os.geteuid() != 0:
            return None
        
        total_watches = 0
        for pid_dir in os.listdir('/proc'):
            try:
                if not pid_dir.isdigit():
                    continue
                
                fd_dir = f'/proc/{pid_dir}/fd'
                if not os.path.exists(fd_dir):
                    continue
                
                for fd in os.listdir(fd_dir):
                    try:
                        link = os.readlink(os.path.join(fd_dir, fd))
                        if 'inotify' in link:
                            # Try to get watch count from the specific inotify instance
                            try:
                                with open(f'/proc/{pid_dir}/status', 'r') as f:
                                    for line in f:
                                        if line.startswith('VmPeak'):
                                            total_watches += 1
                                            break
                            except Exception:
                                pass
                    except Exception:
                        pass
            except Exception:
                pass
        
        return total_watches if total_watches > 0 else None
    except Exception:
        return None


def show_status():
    """Display current inotify status."""
    limits = get_inotify_limits()
    
    if not limits:
        logger.error("❌ Unable to read inotify limits. This may not be a Linux system.")
        return False
    
    logger.info("📊 Inotify Limits & Usage")
    logger.info("─" * 50)
    logger.info(f"Max instances per user:  {limits['max_instances']:>8}")
    if limits['max_watches']:
        logger.info(f"Max watches per user:    {limits['max_watches']:>8}")
    
    logger.info("\n👤 Current Process (TimeMachine daemon)")
    logger.info("─" * 50)
    
    usage = get_inotify_usage()
    if usage is not None:
        logger.info(f"Inotify instances used:  {usage:>8}")
        if limits['max_instances']:
            percent = (usage / limits['max_instances']) * 100
            status = "✅" if percent < 80 else "⚠️ " if percent < 95 else "🔴"
            logger.info(f"Usage: {percent:.1f}% {status}")
    else:
        logger.warning("Unable to determine inotify usage for current process")
    
    return True


def suggest_fix():
    """Show how to increase inotify limits."""
    logger.info("\n🔧 How to Increase Inotify Limits")
    logger.info("─" * 50)
    logger.info("\n1. Temporary fix (until reboot):")
    logger.info("   sudo sysctl -w fs.inotify.max_user_instances=512")
    logger.info("   sudo sysctl -w fs.inotify.max_user_watches=524288")
    logger.info("\n2. Permanent fix (add to /etc/sysctl.conf):")
    logger.info("   fs.inotify.max_user_instances=512")
    logger.info("   fs.inotify.max_user_watches=524288")
    logger.info("   Then run: sudo sysctl -p")
    logger.info("\n3. For systemd user services:")
    logger.info("   Edit ~/.config/systemd/user/timemachine.service (if applicable)")
    logger.info("   Add this after [Unit] section:")
    logger.info("   [Service]")
    logger.info("   LimitNOFILE=infinity")
    logger.info("   Then: systemctl --user daemon-reload")
    
    logger.info("\n💡 Recommendations for TimeMachine:")
    logger.info("   • Set max_watches to 524288+ if backing up large projects")
    logger.info("   • Monitor watched directories for .git, node_modules, etc.")
    logger.info("   • Use config exclusions to avoid watching these heavy dirs")


def main():
    parser = argparse.ArgumentParser(description='Monitor inotify limits and usage')
    parser.add_argument('--suggest-fix', action='store_true', help='Show how to increase limits')
    args = parser.parse_args()
    
    if not show_status():
        return 1
    
    if args.suggest_fix:
        suggest_fix()
    else:
        logger.info("\n💡 Use --suggest-fix to see how to increase inotify limits")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

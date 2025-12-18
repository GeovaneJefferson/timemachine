import psutil
import time
from typing import Dict

# cpu_percent = psutil.cpu_percent(interval=0.1)
# memory_percent = psutil.virtual_memory().percent

# if cpu_percent > 80 or memory_percent > 85:
#     print(10)  # Smaller batches under load
# elif cpu_percent < 30 and memory_percent < 50:
#     print( 00)  # Larger batches when idle
# else:
#     print(50)  # Default


class SystemMonitor:
    """Monitor system load to optimize performance."""
    
    def __init__(self, check_interval: float = 2.0):
        self.check_interval = check_interval
        self.last_check = 0
        self.cpu_load = 0.0
        self.memory_load = 0.0
        self.disk_io_busy = False
        
    def get_current_load(self) -> Dict[str, float]:
        """Get current system load metrics."""
        current_time = time.time()
        
        # Check less frequently to avoid overhead
        if current_time - self.last_check < self.check_interval:
            return {
                'cpu': self.cpu_load,
                'memory': self.memory_load,
                'disk_busy': self.disk_io_busy
            }
        
        try:
            # CPU usage (non-blocking)
            self.cpu_load = psutil.cpu_percent(interval=0.1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.memory_load = memory.percent
            
            # Disk I/O (check if busy)
            disk_io = psutil.disk_io_counters()
            if hasattr(self, '_last_disk_io'):
                # Calculate read/write operations per second
                time_diff = current_time - self.last_check
                read_ops = (disk_io.read_count - self._last_disk_io.read_count) / time_diff
                write_ops = (disk_io.write_count - self._last_disk_io.write_count) / time_diff
                self.disk_io_busy = (read_ops > 50 or write_ops > 50)  # Threshold
            self._last_disk_io = disk_io
            
            self.last_check = current_time
        except Exception:
            pass  # Default to safe values
        
        return {
            'cpu': self.cpu_load,
            'memory': self.memory_load,
            'disk_busy': self.disk_io_busy
        }
    
    def is_system_idle(self) -> bool:
        """Check if system is idle enough for aggressive operations."""
        load = self.get_current_load()
        return (load['cpu'] < 30.0 and 
                load['memory'] < 70.0 and 
                not load['disk_busy'])
    
    def is_system_under_load(self) -> bool:
        """Check if system is under heavy load."""
        load = self.get_current_load()
        return (load['cpu'] > 75.0 or 
                load['memory'] > 85.0 or 
                load['disk_busy'])
    
if __name__ == '__main__':
    monitor = SystemMonitor()
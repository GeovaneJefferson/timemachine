# 🚀 TimeMachine Backup for Linux

A modern, robust backup application for Linux that provides automated, incremental file backup and synchronization via a responsive web-based interface. Tested and optimized on Fedora Linux.

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Web%20Interface-green)](https://flask.palletsprojects.com/)
[![Linux](https://img.shields.io/badge/Platform-Linux-orange)](https://www.linux.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## ✨ Features

| Component | Feature | Description |
|-----------|---------|-------------|
| **Interface** | Modern Web UI | Responsive interface built with HTML/CSS and Tailwind CSS |
| **Backend** | Python & Flask | Robust backend handling all logic and device management |
| **Backup** | Automated & Incremental | Continuous background monitoring, only copies changed files |
| **Optimization** | Hardlink Optimization | Reuses file data on backup target to save space |
| **Monitoring** | Real-time Daemon | Uses watchdog for continuous folder monitoring |
| **Restore** | Hash-based Tracking | Track files across moves and renames using content hashes |
| **Flexibility** | Storage Management | Easy management of external backup storage devices |

## ⚡ Quick Start

### Prerequisites
- Python 3.7+
- Linux system (tested on Fedora)

### Installation

```bash
# Clone the repository
git clone https://github.com/GeovaneJefferson/timemachine.git
cd timemachine

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Start the server
python3 app.py
```

Then open your browser to `http://localhost:5000` and follow the setup wizard.

## 🔧 Architecture

### Project Structure
```
timemachine-electron/
├── config/              # Configuration Files
├── static/              # Web assets (CSS, JS, images)
├── templates/           # HTML templates
├── app.py               # Flask application
├── daemon.py            # Core Backup Daemon
├── server.py            # Shared server functionality
├── search_handler.py    # File search logic
├── storage_util.py      # Storage device detection
├── daemon_control.py    # Daemon management
├── .gitignore
└── requirements.txt
```

### Why Flask?
- **Clean Architecture**: Clear separation of UI from core engine
- **Rapid Development**: Quick iteration without complex native toolkits
- **Remote Access**: Potential for network-based management
- **Learning Platform**: Modern web application patterns

## ⚠️ Important Notes

### Daemon Auto-Start (Not Implemented)
**After every system reboot, you must manually restart the daemon by:**
1. Running `python3 app.py`
2. Opening `http://localhost:5000`
3. Clicking the "RUN" button
4. Or after all its setup, just run daemon.py in terminal :D

### System Compatibility
Designed and tested for Linux systems, primarily Fedora. Other distributions may require adjustments.

## 🛣️ Roadmap

### High Priority
- [ ] Auto startup

### Medium Priority
- [ ] Native UI integration (GTK4/Qt6)
- [ ] System tray icon
- [ ] Desktop notifications

### Low Priority
- [ ] Remote management
- [ ] Multiple backup targets
- [ ] Backup encryption

## 🐛 Troubleshooting

### Common Issues
1. **"Permission denied" errors**
   - Ensure write access to backup target
   - Use appropriate permissions for system folders

2. **Daemon not starting**
   - Check if port 5000 is in use
   - Verify Python dependencies are installed

3. **Device not detected**
   - Ensure storage device is properly mounted
   - Check USB connection if using external drive

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
// src/js/utils/notifications.js

class NotificationSystem {
    constructor() {
        this.notificationQueue = [];
        this.isShowingNotification = false;
    }

    // Toast notification
    showToast(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `global-notification ${type}`;
        
        let icon = 'info';
        switch(type) {
            case 'success': icon = 'check_circle'; break;
            case 'error': icon = 'error'; break;
            case 'warning': icon = 'warning'; break;
            case 'info': icon = 'info'; break;
        }

        notification.innerHTML = `
            <span class="material-icons-round icon">${icon}</span>
            <span>${message}</span>
            <button class="close-btn">
                <span class="material-icons-round">close</span>
            </button>
        `;

        document.body.appendChild(notification);

        // Close button handler
        const closeBtn = notification.querySelector('.close-btn');
        closeBtn.addEventListener('click', () => {
            this.removeNotification(notification);
        });

        // Auto-remove after duration
        setTimeout(() => {
            if (notification.parentNode) {
                this.removeNotification(notification);
            }
        }, duration);
    }

    removeNotification(notification) {
        notification.classList.add('hide');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }

    // Confirmation dialog
    showConfirm(title, message, options = {}) {
        return new Promise((resolve) => {
            const {
                confirmText = 'Confirm',
                cancelText = 'Cancel',
                confirmType = 'primary', // 'primary' or 'danger'
                onConfirm = () => {},
                onCancel = () => {}
            } = options;

            const overlay = document.createElement('div');
            overlay.className = 'confirmation-dialog-overlay';
            
            overlay.innerHTML = `
                <div class="confirmation-dialog">
                    <div class="title">${title}</div>
                    <div class="message">${message}</div>
                    <div class="buttons">
                        <button class="btn btn-cancel">${cancelText}</button>
                        <button class="btn btn-confirm ${confirmType === 'danger' ? 'danger' : ''}">
                            ${confirmText}
                        </button>
                    </div>
                </div>
            `;

            document.body.appendChild(overlay);

            // Get buttons
            const confirmBtn = overlay.querySelector('.btn-confirm');
            const cancelBtn = overlay.querySelector('.btn-cancel');

            // Handle confirm
            const handleConfirm = () => {
                overlay.remove();
                resolve(true);
                onConfirm();
            };

            // Handle cancel
            const handleCancel = () => {
                overlay.remove();
                resolve(false);
                onCancel();
            };

            // Add event listeners
            confirmBtn.addEventListener('click', handleConfirm);
            cancelBtn.addEventListener('click', handleCancel);

            // Close on ESC key
            const handleKeyDown = (e) => {
                if (e.key === 'Escape') {
                    handleCancel();
                }
            };
            document.addEventListener('keydown', handleKeyDown);

            // Cleanup
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    handleCancel();
                }
            });

            // Remove keydown listener when dialog closes
            const originalRemove = overlay.remove;
            overlay.remove = function() {
                document.removeEventListener('keydown', handleKeyDown);
                originalRemove.call(this);
            };
        });
    }

    // Quick methods for common notifications
    success(message, duration = 3000) {
        this.showToast(message, 'success', duration);
    }

    error(message, duration = 3000) {
        this.showToast(message, 'error', duration);
    }

    warning(message, duration = 3000) {
        this.showToast(message, 'warning', duration);
    }

    info(message, duration = 3000) {
        this.showToast(message, 'info', duration);
    }
}

// Create global instance
window.NotificationSystem = new NotificationSystem();

// Shortcut functions for easy access
window.showToast = (message, type, duration) => window.NotificationSystem.showToast(message, type, duration);
window.showConfirm = (title, message, options) => window.NotificationSystem.showConfirm(title, message, options);
window.showSuccess = (message, duration) => window.NotificationSystem.success(message, duration);
window.showError = (message, duration) => window.NotificationSystem.error(message, duration);
window.showWarning = (message, duration) => window.NotificationSystem.warning(message, duration);
window.showInfo = (message, duration) => window.NotificationSystem.info(message, duration);

// Also export functions for module imports (keep globals for legacy callers)
export function showToast(message, type = 'info', duration = 3000) {
    return window.NotificationSystem.showToast(message, type, duration);
}

export function showConfirm(title, message, options = {}) {
    return window.NotificationSystem.showConfirm(title, message, options);
}

export function showSuccess(message, duration = 3000) {
    return window.NotificationSystem.success(message, duration);
}

export function showError(message, duration = 3000) {
    return window.NotificationSystem.error(message, duration);
}

export function showWarning(message, duration = 3000) {
    return window.NotificationSystem.warning(message, duration);
}
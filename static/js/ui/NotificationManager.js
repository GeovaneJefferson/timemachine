/**
 * Manages system notifications/toasts
 */

export class NotificationManager {
    constructor() {
        this.container = document.getElementById('notification-container');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'notification-container';
            this.container.className = 'fixed top-4 right-4 z-50 flex flex-col gap-2 items-end pointer-events-none';
            document.body.appendChild(this.container);
        }
    }

    show(type, title, message, duration = 6000) {
        const toast = document.createElement('div');

        let iconClass = '';
        let colorClass = '';

        switch (type) {
            case 'success':
                iconClass = 'bi-check-circle-fill';
                colorClass = 'bg-green-600 text-white';
                break;
            case 'error':
                iconClass = 'bi-x-octagon-fill';
                colorClass = 'bg-red-500 text-white';
                break;
            case 'info':
            default:
                iconClass = 'bi-info-circle-fill';
                colorClass = 'bg-blue-600 text-white';
                break;
        }

        toast.className = `w-80 p-4 rounded-xl shadow-lg flex items-start gap-3 transition-all transform duration-300 pointer-events-auto opacity-0 -translate-y-full ${colorClass}`;

        toast.innerHTML = `
        <i class="bi ${iconClass} text-xl flex-shrink-0"></i>
        <div class="flex-grow">
        <h5 class="font-bold text-sm">${title}</h5>
        <p class="text-xs opacity-90">${message}</p>
        </div>
        `;

        this.container.appendChild(toast);

        // Animate in
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                toast.classList.remove('opacity-0', '-translate-y-full');
                toast.classList.add('opacity-100', 'translate-y-0');
            });
        });

        // Auto-dismiss
        setTimeout(() => {
            toast.classList.remove('opacity-100', 'translate-y-0');
            toast.classList.add('opacity-0', '-translate-y-full');

            setTimeout(() => {
                if (toast.parentNode === this.container) {
                    this.container.removeChild(toast);
                }
            }, 300);
        }, duration);

        return toast;
    }
}

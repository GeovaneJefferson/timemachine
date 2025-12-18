/**
 * Manages modal dialogs
 */

export class ModalManager {
    constructor(state, eventBus) {
        this.state = state;
        this.eventBus = eventBus;
    }

    showConfirmationModal(options) {
        const {
            title,
            message,
            onConfirm,
            onCancel,
            confirmText = 'Confirm',
            cancelText = 'Cancel',
            confirmColor = 'bg-brand-500',
            showCancel = true
        } = options;

        const modal = document.getElementById('confirmation-modal');
        const modalContainer = document.getElementById('confirmation-modal-container');
        const titleEl = document.getElementById('modal-title');
        const messageEl = document.getElementById('modal-desc');
        const confirmBtn = document.getElementById('modal-confirm-btn');
        const cancelBtn = document.getElementById('modal-cancel-btn');

        if (!modal || !modalContainer || !titleEl || !messageEl || !confirmBtn || !cancelBtn) {
            console.error('[ModalManager] Missing modal elements');
            return;
        }

        // Update content
        titleEl.textContent = title;
        messageEl.innerHTML = message;

        // Setup buttons
        confirmBtn.textContent = confirmText;
        confirmBtn.className = `btn-primary px-4 py-2 rounded-lg ${confirmColor} border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main font-bold transition cursor-pointer`;
        confirmBtn.onclick = () => {
            if (onConfirm) onConfirm();
            this.closeModal();
        };

        cancelBtn.textContent = cancelText;
        cancelBtn.onclick = () => {
            if (onCancel) onCancel();
            this.closeModal();
        };

        if (!showCancel) {
            cancelBtn.classList.add('hidden');
        } else {
            cancelBtn.classList.remove('hidden');
        }

        // Show modal
        modal.classList.remove('hidden');
        modal.classList.add('flex');

        setTimeout(() => {
            modalContainer.classList.remove('opacity-0', 'scale-95');
            modalContainer.classList.add('opacity-100', 'scale-100');
        }, 10);
    }

    showRestoreOptionsModal(fileName, options) {
        let optionsHtml = '';

        options.forEach(option => {
            optionsHtml += `
            <div class="group cursor-pointer" onclick="app.restoreManager.handleRestoreRequest({backupPath: '${option.backupPath}', restoreType: '${option.id}'})">
            <div class="p-4 btn-normal hover:bg-gray-100 dark:hover:bg-white/10 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-amber-500 dark:hover:border-amber-500 hover:shadow-md transition-all duration-200">
            <div class="flex items-center gap-4">
            <div class="flex-shrink-0">
            <div class="w-12 h-12 rounded-lg bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center group-hover:scale-110 transition-transform">
            <i class="bi ${option.icon} text-xl"></i>
            </div>
            </div>
            <div class="flex-1 min-w-0">
            <h4 class="font-bold text-slate-900 dark:text-slate-100 text-sm mb-1">${option.title}</h4>
            <p class="text-xs text-slate-600 dark:text-slate-400 break-all" title="${option.description}">
            ${option.description}
            </p>
            </div>
            <div class="flex-shrink-0">
            <i class="bi bi-chevron-right text-slate-400 group-hover:${option.color.replace('text-', 'text-')} group-hover:translate-x-1 transition-all"></i>
            </div>
            </div>
            </div>
            </div>
            `;
        });

        this.showConfirmationModal({
            title: `Restore "${fileName}"`,
            message: `
            <div class="space-y-4">
            ${optionsHtml}
            </div>
            `,
            showCancel: true,
            cancelText: 'Cancel',
            confirmText: '',
            customButtons: true
        });
    }

    showProgressModal(title, message) {
        this.showConfirmationModal({
            title,
            message: `
            <div class="space-y-4">
            <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center">
            <i class="bi bi-arrow-clockwise animate-spin text-lg"></i>
            </div>
            <div>
            <h4 class="font-bold text-main text-sm">${title}</h4>
            <p class="text-xs text-muted">${message}</p>
            </div>
            </div>
            <div class="space-y-2">
            <div class="flex items-center justify-between text-xs text-muted">
            <span>Processing...</span>
            <span id="modal-progress" class="text-blue-600 font-medium">0%</span>
            </div>
            <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 overflow-hidden">
            <div id="modal-progress-bar" class="bg-blue-500 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
            </div>
            </div>
            </div>
            `,
            showCancel: true,
            cancelText: 'Cancel',
            confirmText: '',
            customButtons: true
        });
    }

    updateProgress(percent, message) {
        const progressBar = document.getElementById('modal-progress-bar');
        const progressText = document.getElementById('modal-progress');

        if (progressBar) {
            progressBar.style.width = `${percent}%`;
        }

        if (progressText) {
            progressText.textContent = `${percent}%`;
        }

        if (message) {
            const messageEl = document.getElementById('modal-desc');
            if (messageEl) {
                const messageContainer = messageEl.querySelector('.text-xs.text-muted');
                if (messageContainer) {
                    messageContainer.textContent = message;
                }
            }
        }
    }

    closeModal() {
        const modal = document.getElementById('confirmation-modal');
        const modalContainer = document.getElementById('confirmation-modal-container');

        if (modal && modalContainer) {
            modalContainer.classList.add('opacity-0', 'scale-95');
            modalContainer.classList.remove('opacity-100', 'scale-100');

            setTimeout(() => {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
            }, 200);
        }
    }
}

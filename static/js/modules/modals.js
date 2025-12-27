/**
 * @file modals.js
 * @description Modal dialog management - confirmation, pro plan, etc.
 */

import { state } from './globals.js';

// =====================================================================
// --- CONFIRMATION MODAL ---
// =====================================================================

export function openConfirmationModal(title, desc, callback, options = {}) {
    const modal = document.getElementById('confirmation-modal');
    const modalContainer = document.getElementById('confirmation-modal-container');
    const titleEl = document.getElementById('modal-title');
    const descEl = document.getElementById('modal-desc');
    const confirmBtn = document.getElementById('modal-confirm-btn');
    const cancelBtn = document.getElementById('modal-cancel-btn');

    console.log('Opening confirmation modal with options:', options);

    if (modal && modalContainer && titleEl && descEl && confirmBtn && cancelBtn) {
        titleEl.innerText = title;
        descEl.innerHTML = desc;

        // Set width based on options
        if (options.wideModal) {
            modalContainer.classList.remove('max-w-lg', 'max-w-md');
            modalContainer.classList.add('max-w-2xl');
        } else if (options.mediumModal) {
            modalContainer.classList.remove('max-w-lg', 'max-w-2xl');
            modalContainer.classList.add('max-w-md');
        } else {
            modalContainer.classList.remove('max-w-md', 'max-w-2xl');
            modalContainer.classList.add('max-w-lg');
        }

        // Handle custom buttons
        if (options.customButtons) {
            confirmBtn.classList.add('hidden');
            cancelBtn.textContent = options.cancelText || 'Cancel';
            cancelBtn.className = "px-4 py-2 rounded-lg border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main font-bold transition cursor-pointer";

            if (options.onCancel) {
                cancelBtn.onclick = () => {
                    closeConfirmModal();
                    options.onCancel();
                };
            } else {
                cancelBtn.onclick = closeConfirmModal;
            }
        } else {
            confirmBtn.classList.remove('hidden');
            confirmBtn.textContent = options.confirmText || 'Confirm';
            cancelBtn.textContent = options.cancelText || 'Cancel';

            const confirmColor = options.confirmColor;
            confirmBtn.className = `btn-primary px-4 py-2 rounded-lg ${confirmColor} border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main font-bold transition cursor-pointer`;
            cancelBtn.className = 'px-4 py-2 rounded-lg border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main font-bold transition cursor-pointer';

            if (options.onConfirm) {
                confirmBtn.onclick = () => {
                    closeConfirmModal();
                    options.onConfirm();
                };
            } else {
                state.pendingAction = callback;
                confirmBtn.onclick = confirmAction;
            }

            if (options.onCancel) {
                cancelBtn.onclick = () => {
                    closeConfirmModal();
                    options.onCancel();
                };
            } else {
                cancelBtn.onclick = closeConfirmModal;
            }
        }

        // Add entrance animation
        modalContainer.classList.remove('opacity-0', 'scale-95');
        modalContainer.classList.add('opacity-100', 'scale-100');

        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

export function closeConfirmModal() {
    const modal = document.getElementById('confirmation-modal');
    const modalContainer = document.getElementById('confirmation-modal-container');

    if (modal && modalContainer) {
        modalContainer.classList.remove('opacity-100', 'scale-100');
        modalContainer.classList.add('opacity-0', 'scale-95');

        setTimeout(() => {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            modalContainer.classList.remove('max-w-md', 'max-w-2xl');
            modalContainer.classList.add('max-w-lg');
        }, 200);

        state.pendingAction = null;
    }
}

export function confirmAction() {
    if (state.pendingAction) state.pendingAction();
    closeConfirmModal();
}

// =====================================================================
// --- PRO PLAN MODAL ---
// =====================================================================

export function openProModal() {
    document.getElementById('pro-modal').classList.remove('hidden');
}

export function closeProModal() {
    document.getElementById('pro-modal').classList.add('hidden');
}

// Make functions globally available
window.openConfirmationModal = openConfirmationModal;
window.closeConfirmModal = closeConfirmModal;
window.confirmAction = confirmAction;
window.openProModal = openProModal;
window.closeProModal = closeProModal;

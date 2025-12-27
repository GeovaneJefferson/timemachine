/**
 * Pro Plan Features Module
 */

import { state } from './globals.js';
import { showSystemNotification } from './ui-helpers.js';

function checkProBeforeRestore() {
    if (state.userPlan === 'pro') {
        startMigrationProcess();
    } else {
        showSystemNotification('info', 'Pro Feature Required', 'Upgrade to Pro to start system restoration.');
        openProPlanModal();
    }
}

function updateRestoreButton() {
    const btn = document.getElementById('btn-start-restore');
    if (!btn) return;

    const hasSelection = Object.values(state.migSelectionState).some(v => v);
    const span = btn.querySelector('span');
    const cancel_restore_btn = document.getElementById('cancel-restore-btn');

    if (state.userPlan === 'pro') {
        if (hasSelection) {
            btn.disabled = false;
            btn.className = "bg-brand-600 text-white hover:bg-brand-700 px-8 py-3 rounded-xl font-bold text-sm transition flex items-center gap-2 shadow-sm cursor-pointer";
            btn.onclick = startMigrationProcess;
            if (cancel_restore_btn) {
                cancel_restore_btn.classList.remove('hidden');
            }
        } else {
            btn.disabled = true;
            btn.className = "bg-slate-200 text-slate-400 dark:bg-slate-700 dark:text-slate-500 px-8 py-3 rounded-xl font-bold text-sm transition cursor-not-allowed flex items-center gap-2";
            btn.onclick = null;
        }
        const starIcon = btn.querySelector('.bi-star-fill');
        if (starIcon) {
            starIcon.remove();
        }
    } else {
        btn.disabled = false;
        btn.className = "bg-gradient-to-r from-brand-600 to-purple-600 text-white hover:from-brand-700 hover:to-purple-700 px-8 py-3 rounded-xl font-bold text-sm transition flex items-center gap-2 shadow-sm cursor-pointer";
        btn.onclick = checkProBeforeRestore;

        const starIcon = btn.querySelector('.bi-star-fill');
        if (!starIcon) {
            const newStarIcon = document.createElement('i');
            newStarIcon.className = 'bi bi-star-fill text-yellow-400 mr-1';
            btn.insertBefore(newStarIcon, btn.querySelector('span'));
        }
    }

    if (span) {
        span.textContent = "Start Restore";
    }
}

function updateUserPlan(plan) {
    state.userPlan = plan;
    updateProUI();
}

function updateProUI() {
    updateRestoreButton();
    updateDashboardStatus();
}

function openProPlanModal() {
    const modal = document.getElementById('pro-plan-modal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        setTimeout(() => {
            modal.style.opacity = '1';
        }, 10);
    }
}

function closeProPlanModal() {
    const modal = document.getElementById('pro-plan-modal');
    if (modal) {
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }, 300);
    }
}

function purchaseProPlan() {
    const button = document.querySelector('#pro-plan-modal button[onclick="purchaseProPlan()"]');
    const originalText = button.innerHTML;

    button.innerHTML = '<i class="bi bi-arrow-clockwise animate-spin mr-2"></i> Processing...';
    button.disabled = true;

    setTimeout(() => {
        state.userPlan = 'pro';
        updateProUI();
        button.innerHTML = '<i class="bi bi-check-lg mr-2"></i> Purchase Successful!';
        button.classList.remove('from-brand-600', 'to-purple-600');
        button.classList.add('bg-green-500', 'text-white');

        setTimeout(() => {
            closeProPlanModal();
            showSystemNotification('success', 'Welcome to Pro!', 'Your Pro Plan features are now active.');
        }, 1500);
    }, 2000);
}

function updateDashboardStatus() {
    const statusBadge = document.getElementById('user-plan-badge');
    const protectionStatus = document.getElementById('protection-status');

    if (!statusBadge || !protectionStatus) return;

    if (state.userPlan === 'pro') {
        statusBadge.textContent = 'Pro';
        statusBadge.className = 'text-xl font-mono font-bold text-purple-200';
        protectionStatus.textContent = 'Advanced protection with unlimited version history & cloud sync.';
        protectionStatus.className = 'text-purple-100 text-sm mt-1';
    } else {
        statusBadge.textContent = 'Basic';
        statusBadge.className = 'text-xl font-mono font-bold text-green-200';
        protectionStatus.textContent = 'Real-time monitoring is active across 4 watched folders.';
        protectionStatus.className = 'text-green-100 text-sm mt-1';
    }
}

export { checkProBeforeRestore, updateRestoreButton, updateUserPlan, updateProUI, openProPlanModal, closeProPlanModal, purchaseProPlan, updateDashboardStatus };

/**
 * Manages UI updates and navigation
 */

export class UIManager {
    constructor(state, eventBus) {
        this.state = state;
        this.eventBus = eventBus;
    }

    navigateToTab(tabId) {
        this.state.navigation.currentTab = tabId;

        // Update sidebar active states
        document.querySelectorAll('.btn-nav').forEach(btn => {
            btn.classList.remove('active', 'bg-blue-50', 'text-blue-600', 'dark:bg-blue-900/20', 'dark:text-blue-400');
            btn.classList.add('text-secondary');
        });

        const targetBtn = document.getElementById(`btn-${tabId}`);
        if (targetBtn) {
            targetBtn.classList.add('active');
            targetBtn.classList.remove('text-secondary');
        }

        // Switch views
        ['overview', 'files', 'devices', 'migration', 'settings', 'logs'].forEach(t => {
            const view = document.getElementById(`view-${t}`);
            if (view) view.classList.add('hidden');
        });

            const targetView = document.getElementById(`view-${tabId}`);
            if (targetView) {
                targetView.classList.remove('hidden');
                targetView.classList.add('animate-entry');
            }

            // Update page title
            const titles = {
                overview: 'Dashboard',
                files: 'File Explorer',
                devices: 'Backup Sources',
                migration: 'System Restore',
                settings: 'Preferences',
                logs: 'Console'
            };

            const titleEl = document.getElementById('page-title');
            if (titleEl) titleEl.innerText = titles[tabId] || 'Dashboard';

            // Trigger lazy loading
            this.eventBus.emit(`tab:${tabId}:activated`);
    }

    updateGreeting() {
        const greetEl = document.getElementById('greeting');
        if (greetEl) {
            greetEl.innerText = `Hello, ${this.state.user.name}`;
        }
    }

    updateDashboardStatus() {
        const statusBadge = document.getElementById('user-plan-badge');
        const protectionStatus = document.getElementById('protection-status');

        if (!statusBadge || !protectionStatus) return;

        if (this.state.user.plan === 'pro') {
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

    updateProUI() {
        this.updateRestoreButton();
        this.updateDashboardStatus();
    }

    updateRestoreButton() {
        const btn = document.getElementById('btn-start-restore');
        if (!btn) return;

        const hasSelection = Object.values(this.state.migration.selectionState).some(v => v);
        const span = btn.querySelector('span');
        const cancelBtn = document.getElementById('cancel-restore-btn');

        if (this.state.user.plan === 'pro') {
            // Pro user
            if (hasSelection) {
                btn.disabled = false;
                btn.className = "bg-brand-600 text-white hover:bg-brand-700 px-8 py-3 rounded-xl font-bold text-sm transition flex items-center gap-2 shadow-sm cursor-pointer";
                btn.onclick = () => this.eventBus.emit('migration:start');

                if (cancelBtn) {
                    cancelBtn.classList.remove('hidden');
                }
            } else {
                btn.disabled = true;
                btn.className = "bg-slate-200 text-slate-400 dark:bg-slate-700 dark:text-slate-500 px-8 py-3 rounded-xl font-bold text-sm transition cursor-not-allowed flex items-center gap-2";
                btn.onclick = null;
            }

            // Remove star icon
            const starIcon = btn.querySelector('.bi-star-fill');
            if (starIcon) starIcon.remove();
        } else {
            // Basic user
            btn.disabled = false;
            btn.className = "bg-gradient-to-r from-brand-600 to-purple-600 text-white hover:from-brand-700 hover:to-purple-700 px-8 py-3 rounded-xl font-bold text-sm transition flex items-center gap-2 shadow-sm cursor-pointer";
            btn.onclick = () => this.checkProBeforeRestore();

            // Ensure star icon exists
            const starIcon = btn.querySelector('.bi-star-fill');
            if (!starIcon) {
                const newStarIcon = document.createElement('i');
                newStarIcon.className = 'bi bi-star-fill text-yellow-400 mr-1';
                btn.insertBefore(newStarIcon, btn.querySelector('span'));
            }
        }

        // Update button text
        if (span) {
            span.textContent = "Start Restore";
        }
    }

    checkProBeforeRestore() {
        if (this.state.user.plan === 'pro') {
            this.eventBus.emit('migration:start');
        } else {
            this.eventBus.emit('notification:show', {
                type: 'info',
                title: 'Pro Feature Required',
                message: 'Upgrade to Pro to start system restoration.'
            });
            this.eventBus.emit('modal:proPlan:open');
        }
    }
}

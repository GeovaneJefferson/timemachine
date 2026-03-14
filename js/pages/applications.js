// src/js/pages/applications.js

import { createListLoadingSkeleton } from '../utils/loading-skeleton.js';

export default class ApplicationsPage {
    constructor() {
        this.name = 'applications';
        this.loading = true;
        this.data = {
            applications: [],
            rawText: ''
        };
        this.loadRealData();
    }

    async loadRealData() {
        try {
            const response = await fetch('/api/applications/list');
            const result = await response.json();
            
            if (result.success) {
                this.data.applications = result.applications || [];
                // backend now sends raw file contents for debugging/inspection
                this.data.rawText = result.raw || '';
            } else {
                console.warn('Failed to load applications:', result.error);
                this.data.applications = [];
                this.data.rawText = '';
            }
        } catch (error) {
            console.error('Error loading applications:', error);
            this.data.applications = [];
            this.data.rawText = '';
        } finally {
            this.loading = false;
            window.applicationsLoaded = true;
            // Update the DOM after data loads
            await this.updateDom();
        }
    }

    async updateDom() {
        const pageContent = document.getElementById('page-content');
        if (pageContent) {
            pageContent.innerHTML = await this.render();
            if (this.afterRender) {
                this.afterRender();
            }
        }
    }

    async render() {
        // Show loading skeleton while fetching data
        if (this.loading) {
            return `
                <div class="px-8 py-6 flex items-end justify-between border-b border-border-light bg-surface-light">
                    <div>
                        <h1 class="text-2xl font-bold text-[var(--color-text-primary)] leading-tight">Installed Applications</h1>
                        <p class="text-sm text-text-secondary-light mt-1">Your installed Flatpak applications are automatically saved for future clean reinstall usage.</p>
                    </div>
                </div>
                <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)]">
                    ${createListLoadingSkeleton(6)}
                </div>
            `;
        }

        // Show empty state if no applications
        if (this.data.applications.length === 0) {
            return `
                <div class="px-8 py-6 flex items-end justify-between border-b border-border-light bg-surface-light">
                    <div>
                        <h1 class="text-2xl font-bold text-[var(--color-text-primary)] leading-tight">Installed Applications</h1>
                        <p class="text-sm text-text-secondary-light mt-1">Your installed Flatpak applications are automatically saved for future clean reinstall usage.</p>
                    </div>
                </div>
                <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)] flex items-center justify-center">
                    <div class="text-center">
                        <span class="material-icons-round text-6xl text-[var(--color-text-secondary)] mb-4 block">apps</span>
                        <p class="text-[var(--color-text-secondary)] text-lg">No Flatpak applications backed up yet</p>
                        <p class="text-[var(--color-text-secondary)] text-sm mt-2">Applications will appear here once the daemon backs them up</p>
                    </div>
                </div>
            `;
        }

        // Show real applications table
        return `
            <div class="px-8 py-6 flex items-end justify-between border-b border-border-light bg-surface-light">
                <div>
                    <h1 class="text-2xl font-bold text-[var(--color-text-primary)] leading-tight">Installed Applications</h1>
                    <p class="text-sm text-text-secondary-light mt-1">Your installed Flatpak applications are automatically saved for future clean reinstall usage.</p>
                </div>
                <button id="refresh-apps-btn" title="Refresh list" class="px-3 py-1 bg-[var(--color-gray-200)] rounded hover:bg-[var(--color-gray-300)]">
                    <span class="material-icons-round">refresh</span>
                </button>
            </div>
            <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)]">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-[var(--color-gray-50)] sticky top-0 z-0 shadow-sm">
                        <tr>
                            <th class="px-6 py-2 text-xs font-semibold text-[var(--color-text-secondary)] border-b border-[var(--color-gray-200)] flex-1">Application Name</th>
                            <th class="px-6 py-2 text-xs font-semibold text-[var(--color-text-secondary)] border-b border-[var(--color-gray-200)] flex-1">Identifier</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-[var(--color-gray-100)] text-sm">
                        ${this.data.applications.map(app => this.renderApplicationRow(app)).join('')}
                    </tbody>
                </table>
            </div>
            <!-- raw file contents section -->
            ${this.data.rawText ? `
            <div class="p-4 bg-[var(--color-gray-50)] border-t border-border-light">
                <h2 class="text-lg font-medium">Raw flatpak_applications.txt</h2>
                <pre class="whitespace-pre-wrap text-xs bg-[var(--color-system-background)] border rounded p-2" id="raw-flatpak-text">${this.data.rawText}</pre>
            </div>
            ` : `
            <div class="p-4 bg-[var(--color-gray-50)] border-t border-border-light text-[var(--color-text-secondary)] text-sm">
                No raw file contents available
            </div>
            `}
        `;
    }

    renderApplicationRow(app) {
        return `
            <tr class="hover:bg-[var(--color-gray-50)] group cursor-default transition-colors">
                <td class="px-6 py-3">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-lg ${app.color} flex items-center justify-center text-white shadow-sm flex-shrink-0 ${app.color === 'bg-[var(--color-gray-800)]' ? 'border border-[var(--color-gray-600)]' : ''}">
                            <span class="material-icons-round text-lg">${app.icon}</span>
                        </div>
                        <span class="font-medium text-[var(--color-text-primary)]">${app.name}</span>
                    </div>
                </td>
                <td class="px-6 py-3">
                    <span class="font-mono text-xs text-text-secondary-light bg-[var(--color-gray-100)] px-2 py-1 rounded border border-[var(--color-gray-200)]">${app.identifier}</span>
                </td>
            </tr>
        `;
    }

    afterRender() {
        console.log('Applications page rendered with', this.data.applications.length, 'applications');
        const btn = document.getElementById('refresh-apps-btn');
        if (btn) {
            btn.addEventListener('click', async () => {
                this.loading = true;
                this.render(); // re-render quickly with loading state
                await this.loadRealData();
                this.updateDom();
            });
        }
    }

    destroy() {
        console.log('Cleaning up Applications page');
    }
}
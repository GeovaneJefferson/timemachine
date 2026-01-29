// src/js/pages/applications.js

import { createListLoadingSkeleton } from '../utils/loading-skeleton.js';

export default class ApplicationsPage {
    constructor() {
        this.name = 'applications';
        this.loading = true;
        this.data = {
            applications: []
        };
        this.loadRealData();
    }

    async loadRealData() {
        try {
            const response = await fetch('/api/applications/list');
            const result = await response.json();
            
            if (result.success) {
                this.data.applications = result.applications || [];
            } else {
                console.warn('Failed to load applications:', result.error);
                this.data.applications = [];
            }
        } catch (error) {
            console.error('Error loading applications:', error);
            this.data.applications = [];
        } finally {
            this.loading = false;
            window.applicationsLoaded = true;
        }
    }

    async render() {
        // Show loading skeleton while fetching data
        if (this.loading) {
            return `
                <div class="px-8 py-6 flex items-end justify-between border-b border-border-light bg-surface-light">
                    <div>
                        <h1 class="text-2xl font-bold text-gray-900 leading-tight">Installed Applications</h1>
                        <p class="text-sm text-text-secondary-light mt-1">Your installed Flatpak applications are automatically saved for future clean reinstall usage.</p>
                    </div>
                </div>
                <div class="flex-1 overflow-y-auto bg-white">
                    ${createListLoadingSkeleton(6)}
                </div>
            `;
        }

        // Show empty state if no applications
        if (this.data.applications.length === 0) {
            return `
                <div class="px-8 py-6 flex items-end justify-between border-b border-border-light bg-surface-light">
                    <div>
                        <h1 class="text-2xl font-bold text-gray-900 leading-tight">Installed Applications</h1>
                        <p class="text-sm text-text-secondary-light mt-1">Your installed Flatpak applications are automatically saved for future clean reinstall usage.</p>
                    </div>
                </div>
                <div class="flex-1 overflow-y-auto bg-white flex items-center justify-center">
                    <div class="text-center">
                        <span class="material-icons-round text-6xl text-gray-300 mb-4 block">apps</span>
                        <p class="text-gray-500 text-lg">No Flatpak applications backed up yet</p>
                        <p class="text-gray-400 text-sm mt-2">Applications will appear here once the daemon backs them up</p>
                    </div>
                </div>
            `;
        }

        // Show real applications table
        return `
            <div class="px-8 py-6 flex items-end justify-between border-b border-border-light bg-surface-light">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900 leading-tight">Installed Applications</h1>
                    <p class="text-sm text-text-secondary-light mt-1">Your installed Flatpak applications are automatically saved for future clean reinstall usage.</p>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto bg-white">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-gray-50 sticky top-0 z-0 shadow-sm">
                        <tr>
                            <th class="px-6 py-2 text-xs font-semibold text-gray-500 border-b border-gray-200 flex-1">Application Name</th>
                            <th class="px-6 py-2 text-xs font-semibold text-gray-500 border-b border-gray-200 flex-1">Identifier</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 text-sm">
                        ${this.data.applications.map(app => this.renderApplicationRow(app)).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    renderApplicationRow(app) {
        return `
            <tr class="hover:bg-gray-50 group cursor-default transition-colors">
                <td class="px-6 py-3">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-lg ${app.color} flex items-center justify-center text-white shadow-sm flex-shrink-0 ${app.color === 'bg-gray-800' ? 'border border-gray-600' : ''}">
                            <span class="material-icons-round text-lg">${app.icon}</span>
                        </div>
                        <span class="font-medium text-gray-900">${app.name}</span>
                    </div>
                </td>
                <td class="px-6 py-3">
                    <span class="font-mono text-xs text-text-secondary-light bg-gray-100 px-2 py-1 rounded border border-gray-200">${app.identifier}</span>
                </td>
            </tr>
        `;
    }

    afterRender() {
        console.log('Applications page rendered with', this.data.applications.length, 'applications');
    }

    destroy() {
        console.log('Cleaning up Applications page');
    }
}
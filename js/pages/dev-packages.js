// devPackages.js - Dev Packages Page Module

import { createListLoadingSkeleton } from '../utils/loading-skeleton.js';

//Bug:
// 1. Make editPackage(id) use the notifications.js. Maybe need to update notifications.js to support entry type

export default class DevPackagesPage {
    constructor() {
        this.name = 'dev-packages';
        this.data = {
            packages: [],
            categories: ["Python", "Node.js", "Rust", "Docker", "Go", "Ruby", "Java"]
        };
        this.loadPackages();
    }

    // Render the entire dev packages page
    async render() {
        return `
            <!-- Page Header Section -->
            ${this.renderHeader()}
            
            <!-- Packages Table -->
            ${this.renderPackagesTable()}
            
            <!-- Empty State (hidden when packages exist) -->
            ${this.renderEmptyState()}
        `;
    }

    // Render the page header
    renderHeader() {
        return `
            <div class="px-8 py-6 flex items-end justify-between border-b border-border-light bg-surface-light">
                <div>
                    <h1 class="text-2xl font-bold text-[var(--color-text-primary)] leading-tight">Dev Packages</h1>
                    <p class="text-sm text-text-secondary-light mt-1">Manually add package names to reinstall later (e.g. pip, npm).</p>
                </div>
                <div class="flex items-center gap-3">
                    <div class="relative flex-grow">
                        <input 
                            class="w-80 pl-4 pr-10 py-2 text-sm bg-[var(--color-system-background)] border border-[var(--color-gray-300)] rounded-lg focus:ring-2 focus:ring-primary focus:border-primary transition-all placeholder-gray-400 text-[var(--color-text-primary)] shadow-sm" 
                            placeholder="e.g. pip install requests" 
                            type="text"
                            id="package-input"
                        />
                        <button 
                            class="absolute right-1.5 top-1.5 p-0.5 text-primary hover:text-[var(--color-accent)] transition-colors"
                            id="add-package-btn"
                        >
                            <span class="material-icons-round text-lg">add_circle</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // Render the packages table
    renderPackagesTable() {
        return `
            <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)]">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-[var(--color-gray-50)] sticky top-0 z-0 shadow-sm">
                        <tr>
                            <th class="px-6 py-2 text-xs font-semibold text-[var(--color-text-secondary)] border-b border-[var(--color-gray-200)] w-1/2">Package Command / Name</th>
                            <th class="px-6 py-2 text-xs font-semibold text-[var(--color-text-secondary)] border-b border-[var(--color-gray-200)]">Category</th>
                            <th class="px-6 py-2 text-xs font-semibold text-[var(--color-text-secondary)] border-b border-[var(--color-gray-200)]">Date Added</th>
                            <th class="px-6 py-2 text-xs font-semibold text-[var(--color-text-secondary)] border-b border-[var(--color-gray-200)] w-10"></th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 text-sm" id="packages-table-body">
                        ${this.data.packages.map(pkg => this.renderPackageRow(pkg)).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    // Render a single package row
    renderPackageRow(pkg) {
        const colorClasses = {
            yellow: 'bg-[var(--color-gray-50)]/10 text-yellow-500 border-[var(--color-gray-200)]',
            blue: 'bg-[var(--color-accent)]/10 text-[var(--color-accent)] border-[var(--color-accent)]',
            red: 'bg-[var(--color-status-error-bg)]/10 text-[var(--color-status-error)] border-[var(--color-status-error)]',
            purple: 'bg-[var(--color-gray-50)]/10 text-purple-600 border-[var(--color-gray-200)]',
            gray: 'bg-[var(--color-gray-800)] text-white border-[var(--color-gray-600)]'
        };

        const categoryClasses = {
            Python: 'bg-[var(--color-gray-50)] text-[var(--color-accent)] border-[var(--color-accent)]',
            'Node.js': 'bg-[var(--color-gray-50)] text-yellow-500 border-[var(--color-gray-100)]',
            Rust: 'bg-[var(--color-gray-50)] text-orange-500 border-[var(--color-gray-100)]',
            Docker: 'bg-[var(--color-gray-100)] text-[var(--color-text-secondary)] border-[var(--color-gray-200)]'
        };

        return `
            <tr class="hover:bg-[var(--color-gray-50)] group cursor-default transition-colors package-row" 
                data-id="${pkg.id}"
                data-command="${pkg.command}"
                data-category="${pkg.category}">
                <td class="px-6 py-3 whitespace-nowrap">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-lg ${colorClasses[pkg.color]} flex items-center justify-center border shadow-sm">
                            <span class="material-icons-round text-lg">${pkg.icon}</span>
                        </div>
                        <span class="font-mono text-[var(--color-text-primary)]">${pkg.command}</span>
                    </div>
                </td>
                <td class="px-6 py-3 whitespace-nowrap">
                    <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium ${categoryClasses[pkg.category] || 'bg-[var(--color-gray-50)] text-[var(--color-text-secondary)] border-[var(--color-gray-200)]'}">
                        ${pkg.category}
                    </span>
                </td>
                <td class="px-6 py-3 text-[var(--color-text-secondary)] whitespace-nowrap">${pkg.date}</td>
                <td class="px-6 py-3 whitespace-nowrap text-right">
                    <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button class="text-[var(--color-text-secondary)] hover:text-[var(--color-accent)] transition-colors edit-package-btn" data-id="${pkg.id}">
                            <span class="material-icons-round text-lg">edit</span>
                        </button>
                        <button class="text-[var(--color-text-secondary)] hover:text-[var(--color-status-error)] transition-colors delete-package-btn" data-id="${pkg.id}">
                            <span class="material-icons-round text-lg">delete</span>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }

    // Render empty state
    renderEmptyState() {
        return `
            <div class="p-8 text-center ${this.data.packages.length > 0 ? 'hidden' : ''}" id="empty-state">
                <div class="w-16 h-16 bg-[var(--color-gray-50)] rounded-full flex items-center justify-center mx-auto mb-4 border border-[var(--color-gray-100)]">
                    <span class="material-icons-round text-[var(--color-text-secondary)] text-3xl">playlist_add</span>
                </div>
                <h3 class="text-[var(--color-text-primary)] font-medium">No packages added</h3>
                <p class="text-[var(--color-text-secondary)] text-sm mt-1">Add your development packages above to keep track of them.</p>
            </div>
        `;
    }

    // Initialize dev packages page functionality
    afterRender() {
        this.attachEventListeners();
        console.log('Dev Packages page initialized');
    }

    // Attach event listeners
    attachEventListeners() {
        // Add package button
        const addButton = document.getElementById('add-package-btn');
        const packageInput = document.getElementById('package-input');

        if (addButton && packageInput) {
            addButton.addEventListener('click', () => this.addPackage());
            packageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.addPackage();
                }
            });
        }

        // Edit and delete buttons
        document.querySelectorAll('.edit-package-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const id = parseInt(btn.getAttribute('data-id'));
                this.editPackage(id);
            });
        });

        document.querySelectorAll('.delete-package-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const id = parseInt(btn.getAttribute('data-id'));
                this.deletePackage(id);
            });
        });

        // Row click for selection
        document.querySelectorAll('.package-row').forEach(row => {
            row.addEventListener('click', (e) => {
                if (!e.target.closest('button')) {
                    this.selectPackage(row);
                }
            });
        });
    }

    // Add a new package
    addPackage() {
        const input = document.getElementById('package-input');
        const command = input.value.trim();

        if (!command) {
            alert('Please enter a package command');
            return;
        }

        const category = this.detectCategory(command);
        const newPackage = {
            id: Date.now(),
            command: command,
            category: category,
            date: "Today",
            icon: this.getIconForCategory(category),
            color: this.getColorForCategory(category)
        };

        this.data.packages.unshift(newPackage);
        this.updatePackagesTable();
        this.savePackages();
        input.value = '';
        console.log('Package added:', newPackage);
    }

    // Edit a package
    editPackage(id) {
        const pkg = this.data.packages.find(p => p.id === id);
        if (!pkg) return;

        const newCommand = prompt('Edit package command:', pkg.command);
        if (newCommand !== null && newCommand.trim() !== '') {
            pkg.command = newCommand.trim();
            pkg.category = this.detectCategory(newCommand);
            pkg.icon = this.getIconForCategory(pkg.category);
            pkg.color = this.getColorForCategory(pkg.category);
            
            this.updatePackagesTable();
            this.savePackages();
            console.log('Package updated:', pkg);
        }
    }

    // Delete a package
    deletePackage(id) {
        if (confirm('Are you sure you want to delete this package?')) {
            this.data.packages = this.data.packages.filter(p => p.id !== id);
            this.updatePackagesTable();
            this.savePackages();
            console.log('Package deleted:', id);
        }
    }

    savePackages() {
        // Always save locally first for immediate responsiveness
        try {
            localStorage.setItem('devPackages', JSON.stringify(this.data.packages));
        } catch (e) {}

        // Attempt to persist to backend; fail silently but log for debugging
        try {
            fetch('/api/dev-packages', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ packages: this.data.packages })
            }).then(resp => resp.json())
            .then(data => {
                if (!data.success) {
                    console.warn('Failed to save dev packages to server:', data.error);
                    if (window.showError) window.showError('Failed to save dev packages');
                } else {
                    if (window.showSuccess) window.showSuccess('Dev packages saved');
                }
            }).catch(err => {
                console.warn('Error saving dev packages to server:', err);
                if (window.showError) window.showError('Error saving dev packages');
            });
        } catch (e) {
            console.warn('Could not save dev packages to server', e);
            if (window.showError) window.showError('Could not save dev packages');
        }
    }

    loadPackages() {
        try {
            const raw = localStorage.getItem('devPackages');
            if (raw) {
                this.data.packages = JSON.parse(raw);
            }
        } catch (e) {
            console.error('Failed to load dev packages from storage', e);
        }
        // Refresh from server in background and update UI if present
        try {
            fetch('/api/dev-packages')
            .then(r => r.json())
            .then(info => {
                if (info && info.success && Array.isArray(info.packages)) {
                    this.data.packages = info.packages;
                    this.updatePackagesTable();
                    try { localStorage.setItem('devPackages', JSON.stringify(this.data.packages)); } catch (e) {}
                }
            }).catch(err => {
                console.debug('No dev packages on server or fetch failed:', err);
            });
        } catch (e) {
            console.debug('Failed to fetch dev packages from server', e);
        }
    }

    // Select a package row
    selectPackage(row) {
        // Remove previous selection
        document.querySelectorAll('.package-row').forEach(r => {
            r.classList.remove('bg-[var(--color-gray-50)]', 'border-l-4', 'border-l-primary');
        });
        
        // Add selection to clicked row
        row.classList.add('bg-[var(--color-gray-50)]', 'border-l-4', 'border-l-primary');
        
        const id = parseInt(row.getAttribute('data-id'));
        const command = row.getAttribute('data-command');
        console.log('Selected package:', { id, command });
    }

    // Update packages table in DOM
    updatePackagesTable() {
        const tableBody = document.getElementById('packages-table-body');
        const emptyState = document.getElementById('empty-state');
        
        if (tableBody) {
            tableBody.innerHTML = this.data.packages.map(pkg => this.renderPackageRow(pkg)).join('');
        }
        
        if (emptyState) {
            emptyState.classList.toggle('hidden', this.data.packages.length > 0);
        }
        
        // Re-attach event listeners to new elements
        this.attachEventListeners();
    }

    // Detect category from command
    detectCategory(command) {
        const lowerCommand = command.toLowerCase();
        
        if (lowerCommand.includes('pip install') || lowerCommand.includes('python') || lowerCommand.includes('py')) {
            return 'Python';
        } else if (lowerCommand.includes('npm install') || lowerCommand.includes('yarn add') || lowerCommand.includes('node')) {
            return 'Node.js';
        } else if (lowerCommand.includes('cargo install') || lowerCommand.includes('rust')) {
            return 'Rust';
        } else if (lowerCommand.includes('docker') || lowerCommand.includes('container')) {
            return 'Docker';
        } else if (lowerCommand.includes('go get') || lowerCommand.includes('golang')) {
            return 'Go';
        } else if (lowerCommand.includes('gem install') || lowerCommand.includes('ruby')) {
            return 'Ruby';
        } else if (lowerCommand.includes('mvn') || lowerCommand.includes('java')) {
            return 'Java';
        }
        
        return 'Other';
    }

    // Get icon for category
    getIconForCategory(category) {
        const icons = {
            'Python': 'api',
            'Node.js': 'javascript',
            'Rust': 'terminal',
            'Docker': 'layers',
            'Go': 'code',
            'Ruby': 'diamond',
            'Java': 'coffee',
            'Other': 'extension'
        };
        return icons[category] || 'extension';
    }

    // Get color for category
    getColorForCategory(category) {
        const colors = {
            'Python': 'blue',
            'Node.js': 'red',
            'Rust': 'purple',
            'Docker': 'gray',
            'Go': 'blue',
            'Ruby': 'red',
            'Java': 'orange',
            'Other': 'gray'
        };
        return colors[category] || 'gray';
    }

    // Get dev packages data (could be from API)
    async fetchData() {
        // Simulate API call
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(this.data);
            }, 300);
        });
    }

    // Cleanup when leaving page
    destroy() {
        console.log('Dev Packages page destroyed');
        // Clean up any event listeners
    }
}

// Export a function to create dev packages page
export function createDevPackagesPage() {
    return new DevPackagesPage();
}

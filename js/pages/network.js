// src/js/pages/network.js

export default class NetworkPage {
    constructor() {
        this.name = 'network';
        this.loading = false;

        // Sample devices to show in the UI (replace with API data later)
        this.devices = [
            { name: 'Synology-NAS-01', type: 'NAS Server', ip: '192.168.1.100', capacity: '8.2 TB Free', status: 'Available', statusColor: 'green', action: 'connect' },
            { name: 'Creative-Share', type: 'Shared Folder', ip: '192.168.1.45', capacity: '1.5 TB Free', status: 'Connected', statusColor: 'blue', action: 'manage' },
            { name: 'Mac-Studio-Design', type: 'Workstation', ip: '192.168.1.88', capacity: '500 GB Free', status: 'Available', statusColor: 'green', action: 'connect' },
            { name: 'Old-Backup-Server', type: 'Linux Server', ip: '192.168.1.15', capacity: '--', status: 'Offline', statusColor: 'gray', action: 'none' }
        ];

        this.filterText = '';
    }

    renderHeader() {
        return `
        <div class="px-8 py-6 bg-surface-light dark:bg-surface-dark border-b border-border-light dark:border-border-dark flex items-center justify-between">
            <div class="flex items-start gap-6">
                <div class="w-14 h-14 rounded-lg bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center shadow-soft border border-gray-200 dark:border-gray-600">
                    <span class="material-icons-round text-3xl text-gray-700">public</span>
                </div>
                <div>
                    <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Network Locations</h1>
                    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">Select a network device to configure as your backup destination. You can connect to NAS drives, local servers, or other computers on your local network.</p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <div class="text-sm text-text-secondary-light mr-3">Wi‑Fi: Connected</div>
                <div class="text-sm text-text-secondary-light mr-4">Gateway: 192.168.1.1</div>
                <div class="px-3 py-1 rounded-full bg-green-50 text-green-700 text-sm">Scanning Active</div>
            </div>
        </div>
        `;
    }

    renderTableRows() {
        const filter = this.filterText.toLowerCase();
        return this.devices
            .filter(d => !filter || d.name.toLowerCase().includes(filter) || d.ip.includes(filter))
            .map(d => {
                const statusDot = d.statusColor === 'green' ? 'bg-green-500' : d.statusColor === 'blue' ? 'bg-blue-500' : 'bg-gray-400';
                const actionBtn = d.action === 'connect' ? `<button class="connect-btn px-3 py-1 rounded bg-blue-600 text-white text-sm" data-ip="${d.ip}">Connect</button>` :
                                  d.action === 'manage' ? `<button class="manage-btn px-3 py-1 rounded bg-gray-100 text-sm" data-ip="${d.ip}">Manage</button>` :
                                  `<button class="px-3 py-1 rounded bg-gray-200 text-sm text-gray-500" disabled>Connect</button>`;

                return `
                <tr class="hover:bg-gray-50">
                    <td class="px-4 py-3">
                        <div class="flex items-center gap-3">
                            <input type="radio" name="selected-device" data-ip="${d.ip}" />
                            <div>
                                <div class="font-medium text-gray-900 dark:text-white">${d.name}</div>
                                <div class="text-xs text-text-secondary-light dark:text-text-secondary-dark">${d.type}</div>
                            </div>
                        </div>
                    </td>
                    <td class="px-4 py-3 text-sm text-gray-600">${d.type}</td>
                    <td class="px-4 py-3 text-sm text-gray-600">${d.ip}</td>
                    <td class="px-4 py-3 text-sm text-gray-600">${d.capacity}</td>
                    <td class="px-4 py-3 text-sm">
                        <div class="flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full ${statusDot}"></span>
                            <span class="text-sm text-text-secondary-light">${d.status}</span>
                        </div>
                    </td>
                    <td class="px-4 py-3 text-right">${actionBtn}</td>
                </tr>
                `;
            }).join('');
    }

    render() {
        return `
        <div class="flex flex-col h-full overflow-hidden">
            ${this.renderHeader()}
            <div class="px-6 py-4 bg-white dark:bg-surface-dark border-b border-border-light dark:border-border-dark flex items-center gap-3">
                <div class="flex items-center bg-gray-100 dark:bg-gray-800 rounded px-3 py-1 flex-1">
                    <span class="material-icons-round text-gray-400">search</span>
                    <input id="network-search" class="ml-2 bg-transparent outline-none w-full text-sm" placeholder="Search network locations or IP..." />
                </div>
                <button id="add-server-btn" class="px-3 py-1 rounded bg-white border border-gray-200 text-sm">+ Add Server</button>
            </div>

            <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark p-6">
                <div class="text-sm text-text-secondary-light mb-3">Sorted by: Availability</div>
                <div class="overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700">
                    <table class="w-full text-left">
                        <thead class="bg-gray-50 dark:bg-gray-800">
                            <tr>
                                <th class="px-4 py-3">Device Name</th>
                                <th class="px-4 py-3">Type</th>
                                <th class="px-4 py-3">IP Address</th>
                                <th class="px-4 py-3">Capacity</th>
                                <th class="px-4 py-3">Status</th>
                                <th class="px-4 py-3 text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody id="network-table-body">
                            ${this.renderTableRows()}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="px-6 py-3 bg-gray-50 dark:bg-gray-800 text-xs text-text-secondary-light border-t border-border-light dark:border-border-dark">
                4 devices found
            </div>
        </div>
        `;
    }

    async afterRender() {
        // Attach search handler
        const input = document.getElementById('network-search');
        if (input) {
            input.addEventListener('input', (e) => {
                this.filterText = e.target.value;
                const body = document.getElementById('network-table-body');
                if (body) body.innerHTML = this.renderTableRows();
                this.setupActionListeners();
            });
        }

        document.getElementById('add-server-btn')?.addEventListener('click', () => {
            showInfo('Add Server dialog not implemented', 'info');
        });

        this.setupActionListeners();
    }

    setupActionListeners() {
        document.querySelectorAll('.connect-btn').forEach(btn => {
            btn.removeEventListener('click', this._connectHandler);
            btn.addEventListener('click', (e) => {
                const ip = e.currentTarget.getAttribute('data-ip');
                showInfo(`Connecting to ${ip}...`, 'info');
            });
        });

        document.querySelectorAll('.manage-btn').forEach(btn => {
            btn.removeEventListener('click', this._manageHandler);
            btn.addEventListener('click', (e) => {
                const ip = e.currentTarget.getAttribute('data-ip');
                showInfo(`Opening manage dialog for ${ip}...`, 'info');
            });
        });
    }
}

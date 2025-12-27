/**
 * File Explorer & Restoration Module
 */

import { state } from './globals.js';
import { showSystemNotification } from './ui-helpers.js';
import { getIconForFile, getColorForFile, formatBytes, formatRelativeDate } from './utils.js';

async function loadFolderContents(folderPath = '') {
    const container = document.getElementById('file-list-container');
    if (!container) return;

    // Show loading state
    container.innerHTML = `
    <div class="p-8 text-center">
    <i class="bi bi-arrow-clockwise animate-spin text-3xl mb-3 text-brand-500"></i>
    <p class="text-muted">Loading files...</p>
    </div>
    `;

    try {
        const response = await fetch('/api/files/list', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: folderPath })
        });

        const data = await response.json();

        if (data.success && data.files) {
            renderFiles(data.files, container);
        } else {
            container.innerHTML = `
            <div class="p-8 text-center text-muted">
            <i class="bi bi-folder-x text-3xl mb-3"></i>
            <h4 class="font-bold text-main">No Files Found</h4>
            <p class="text-sm mt-1">${data.error || 'No files in this directory'}</p>
            </div>
            `;
        }
    } catch (error) {
        console.error('Error loading files:', error);
        container.innerHTML = `
        <div class="p-8 text-center text-red-500">
        <i class="bi bi-exclamation-triangle-fill text-3xl mb-3"></i>
        <h4 class="font-bold">Failed to Load Files</h4>
        <p class="text-sm mt-1">${error.message || 'Network error'}</p>
        </div>
        `;
    }
}

function renderFiles(files, container) {
    if (files.length === 0) {
        container.innerHTML = `
        <div class="p-8 text-center text-muted">
        <i class="bi bi-inbox text-3xl mb-3"></i>
        <h4 class="font-bold text-main">Empty Folder</h4>
        <p class="text-sm mt-1">This folder is empty</p>
        </div>
        `;
        return;
    }

    let html = `
    <div class="overflow-x-auto">
    <table class="w-full">
    <thead>
    <tr class="text-left text-xs text-secondary border-b border-main">
    <th class="pb-3 pl-6 pr-3 font-semibold">Name</th>
    <th class="pb-3 px-3 font-semibold">Modified</th>
    <th class="pb-3 px-3 font-semibold">Size</th>
    <th class="pb-3 pl-3 pr-6 font-semibold">Actions</th>
    </tr>
    </thead>
    <tbody>
    `;

    files.forEach((file, index) => {
        const icon = getIconForFile(file.name);
        const color = getColorForFile(file.name);
        const modified = formatRelativeDate(file.modified || file.created || '');
        const size = file.size ? formatBytes(file.size) : '—';
        const isFolder = file.type === 'folder' || file.type === 'directory';

        html += `
        <tr class="hover:bg-gray-50 dark:hover:bg-white/5 border-b border-main/10">
        <td class="py-4 pl-6 pr-3">
        <div class="flex items-center gap-3">
        <i class="bi ${icon} ${color} text-lg"></i>
        <div>
        <span class="font-medium text-main">${file.name}</span>
        ${isFolder ? '<span class="text-xs text-muted ml-2">Folder</span>' : ''}
        </div>
        </div>
        </td>
        <td class="py-4 px-3 text-sm text-muted">${modified}</td>
        <td class="py-4 px-3 text-sm text-muted">${size}</td>
        <td class="py-4 pl-3 pr-6">
        ${isFolder ?
            `<button class="text-xs text-brand-600 hover:text-brand-700 font-medium" onclick="loadFolderContents('${file.path || file.name}')">
            Open
            </button>` :
            `<button class="text-xs text-brand-600 hover:text-brand-700 font-medium" onclick="restoreFile('${file.name}')">
            Restore
            </button>`
        }
        </td>
        </tr>
        `;
    });

    html += `
    </tbody>
    </table>
    </div>
    `;

    container.innerHTML = html;
}

function restoreFile(fileName) {
    showSystemNotification('info', 'Restore Requested', `Restoring ${fileName}...`);
    // Implement restore functionality
    console.log('Restoring file:', fileName);
}

export { loadFolderContents, restoreFile };

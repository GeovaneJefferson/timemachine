/**
 * @file file-system.js
 * @description File system initialization and management
 */

import { state } from './globals.js';

// =====================================================================
// --- FILE SYSTEM INITIALIZATION ---
// =====================================================================

async function initializeFileSystem() {
    try {
        // Step 1: Trigger backend file scanning
        const initResponse = await fetch('/api/search/init', { method: 'POST' });
        const initData = await initResponse.json();

        // Step 2: Create the fileSystem root structure
        state.fileSystem = {
            name: '.main_backup',
            type: 'folder',
            children: []
        };

        // Step 3: Initialize navigation stack
        state.breadcrumbStack = [state.fileSystem];
        state.currentFolder = state.fileSystem;

        console.log('[FileSystem] Ready for file operations');
    } catch (error) {
        console.error('[FileSystem] Failed to initialize:', error);
        // Fallback: Create empty fileSystem
        state.fileSystem = {
            name: '.main_backup',
            type: 'folder',
            children: []
        };
        state.breadcrumbStack = [state.fileSystem];
        state.currentFolder = state.fileSystem;
    }
}

// =====================================================================
// --- EXPORTS ---
// =====================================================================

export { initializeFileSystem };

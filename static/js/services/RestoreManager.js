/**
 * Handles file restoration operations
 */

import { ModalManager } from '../ui/ModalManager.js';
import { FileUtils } from '../utils/FileUtils.js';

export class RestoreManager {
    constructor(state, api, eventBus) {
        this.state = state;
        this.api = api;
        this.eventBus = eventBus;
        this.modalManager = new ModalManager(state, eventBus);
    }

    async showRestoreOptions(backupPath, fileName) {
        try {
            const fileInfo = await this.api.getFileInfo(backupPath);

            if (!fileInfo.success) {
                throw new Error('Failed to get file information');
            }

            const options = this.getRestoreOptions(fileInfo, backupPath, fileName);
            this.modalManager.showRestoreOptionsModal(fileName, options);
        } catch (error) {
            console.error('[RestoreManager] Failed to show restore options:', error);
            this.eventBus.emit('notification:show', {
                type: 'error',
                title: 'Restore Error',
                message: 'Failed to get file information'
            });
        }
    }

    getRestoreOptions(fileInfo, backupPath, fileName) {
        const options = [];

        if (fileInfo.exists) {
            if (fileInfo.is_moved) {
                // File exists but was moved
                options.push({
                    id: 'current',
                    title: 'Restore to Current Location',
                    description: fileInfo.actual_path || 'Current location',
                    icon: 'bi-geo-alt-fill',
                    color: 'text-blue-500',
                    action: () => this.restoreToCurrent(backupPath, fileInfo)
                });

                options.push({
                    id: 'original',
                    title: 'Restore to Original Location',
                    description: fileInfo.home_path || 'Original location',
                    icon: 'bi-house-fill',
                    color: 'text-amber-500',
                    action: () => this.restoreToOriginal(backupPath, fileInfo)
                });
            } else {
                // File exists in expected location
                options.push({
                    id: 'original',
                    title: 'Restore File',
                    description: fileInfo.actual_path || fileInfo.home_path || 'Current location',
                    icon: 'bi-house-fill',
                    color: 'text-emerald-500',
                    action: () => this.restoreToOriginal(backupPath, fileInfo)
                });
            }
        } else {
            // File doesn't exist
            options.push({
                id: 'search',
                title: 'Search for Moved File',
                description: 'Search home directory for moved file',
                icon: 'bi-search',
                color: 'text-yellow-500',
                action: () => this.searchForFile(backupPath, fileName)
            });

            options.push({
                id: 'original',
                title: 'Restore to Original Location',
                description: fileInfo.home_path || 'Original location',
                icon: 'bi-house-fill',
                color: 'text-blue-500',
                action: () => this.restoreToOriginal(backupPath, fileInfo)
            });
        }

        return options;
    }

    async restoreToCurrent(backupPath, fileInfo) {
        this.modalManager.showProgressModal('Restoring File', 'Restoring to current location...');

        try {
            const result = await this.api.restoreFile(backupPath, 'current');

            if (result.success) {
                this.modalManager.closeModal();
                this.eventBus.emit('notification:show', {
                    type: 'success',
                    title: 'File Restored',
                    message: 'File has been restored to current location'
                });

                // Refresh file preview if open
                if (this.state.files.selectedFile) {
                    this.eventBus.emit('file:selected', this.state.files.selectedFile);
                }
            } else {
                throw new Error(result.error || 'Restoration failed');
            }
        } catch (error) {
            this.modalManager.closeModal();
            this.eventBus.emit('notification:show', {
                type: 'error',
                title: 'Restoration Failed',
                message: error.message
            });
        }
    }

    async restoreToOriginal(backupPath, fileInfo) {
        // Check if file already exists at original location
        if (fileInfo.exists && !fileInfo.is_moved) {
            const confirmed = await this.modalManager.showConfirmationModal(
                'Overwrite File?',
                'File already exists at this location. Overwrite?',
                { confirmText: 'Overwrite', confirmColor: 'bg-amber-500' }
            );

            if (!confirmed) return;
        }

        this.modalManager.showProgressModal('Restoring File', 'Restoring to original location...');

        try {
            const result = await this.api.restoreFile(backupPath, 'original');

            if (result.success) {
                this.modalManager.closeModal();
                this.eventBus.emit('notification:show', {
                    type: 'success',
                    title: 'File Restored',
                    message: 'File has been restored to original location'
                });

                // Refresh file preview if open
                if (this.state.files.selectedFile) {
                    this.eventBus.emit('file:selected', this.state.files.selectedFile);
                }
            } else {
                throw new Error(result.error || 'Restoration failed');
            }
        } catch (error) {
            this.modalManager.closeModal();
            this.eventBus.emit('notification:show', {
                type: 'error',
                title: 'Restoration Failed',
                message: error.message
            });
        }
    }

    async searchForFile(backupPath, fileName) {
        this.modalManager.showProgressModal('Searching for File', 'Searching home directory...');

        try {
            const result = await this.api.searchMovedFile(backupPath, true);

            if (result.success && result.found) {
                this.modalManager.closeModal();

                const confirmed = await this.modalManager.showConfirmationModal(
                    'File Found',
                    `File found at: ${result.current_location}\n\nRestore to this location?`,
                    { confirmText: 'Restore Here' }
                );

                if (confirmed) {
                    await this.restoreToCurrent(backupPath, result);
                }
            } else {
                this.modalManager.closeModal();
                this.modalManager.showConfirmationModal(
                    'File Not Found',
                    'File was not found in home directory.',
                    { showCancel: false, confirmText: 'OK' }
                );
            }
        } catch (error) {
            this.modalManager.closeModal();
            this.eventBus.emit('notification:show', {
                type: 'error',
                title: 'Search Failed',
                message: error.message
            });
        }
    }

    handleRestoreRequest(data) {
        const { backupPath, restoreType, fileName } = data;

        switch (restoreType) {
            case 'current':
                this.restoreToCurrent(backupPath);
                break;
            case 'original':
                this.restoreToOriginal(backupPath);
                break;
            case 'search':
                this.searchForFile(backupPath, fileName);
                break;
        }
    }
}

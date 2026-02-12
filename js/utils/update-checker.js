// js/utils/update-checker.js

import { showToast } from './notifications.js';

export async function checkUpdates(showUpToDateMessage = false) {
    console.log('Checking for updates...');

    try {
        const response = await fetch('/api/check-for-updates');
        const updateInfo = await response.json();
        
        if (updateInfo.success) {
            if (updateInfo.update_available) {
                const message = `New update available! ${updateInfo.latest_version}`;
                showToast(message, 'success', 10000);

                if (updateInfo.release_url) {
                    const toastElement = document.querySelector('.global-notification');
                    if(toastElement) {
                        toastElement.style.cursor = 'pointer';
                        toastElement.addEventListener('click', () => {
                            window.open(updateInfo.release_url, '_blank');
                        });
                    }
                }
            } else {
                if (showUpToDateMessage) {
                    showToast('You are up to date! (Commit: ' + updateInfo.current_version + ')', 'info');
                }
            }
        } else {
            if (showUpToDateMessage) {
                showToast(`Error: ${updateInfo.error}`, 'error');
            }
            console.error('Error checking for updates:', updateInfo.error);
        }
    } catch (error) {
        if (showUpToDateMessage) {
            showToast('Could not connect to the server to check for updates.', 'error');
        }
        console.error('Failed to check for updates:', error);
    }
}

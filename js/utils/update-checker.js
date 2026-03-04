// js/utils/update-checker.js

import { showToast } from './notifications.js';

export async function checkUpdates() {
    console.log('Checking for updates...');

    try {
        const response = await fetch('/api/check-for-updates');
        const updateInfo = await response.json();
        
        if (updateInfo.success) {
            if (updateInfo.update_available) {
                const message = `New update available! ${updateInfo.latest_version}`;
                showToast(message, 'success', 10000, [
                    {
                        label: 'Tell me more',
                        action: () => {
                            window.open('https://github.com/GeovaneJefferson/timemachine', '_blank');
                        }
                    }
                ]);
            }
        } else {
            console.error('Error checking for updates:', updateInfo.error);
        }
    } catch (error) {
        console.error('Failed to check for updates:', error);
    }
}

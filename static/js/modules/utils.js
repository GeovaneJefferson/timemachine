/**
 * @file utils.js
 * @description Utility functions for formatting, icons, and helpers
 */

// =====================================================================
// --- UTILITY FUNCTIONS ---
// =====================================================================

export class Utils {
    static formatBytes(bytes, decimals = 2) {
        const safeBytes = Number(bytes);
        if (isNaN(safeBytes) || safeBytes <= 0) return '0 Bytes';

        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(safeBytes) / Math.log(k));
        const effectiveIndex = Math.min(i, sizes.length - 1);

        return parseFloat((safeBytes / Math.pow(k, effectiveIndex)).toFixed(decimals)) + ' ' + sizes[effectiveIndex];
    }

    static getUsageColorClass(percent) {
        if (percent > 90) return 'bg-red-500';
        if (percent > 70) return 'bg-yellow-500';
        return 'bg-green-500';
    }

    static handleResponse(response) {
        if (response.status === 204) return null;

        return response.json().then(data => {
            if (data.hasOwnProperty('success') && !data.success) {
                const errorMsg = data.error || 'Request failed';
                console.error('API error:', errorMsg);
                throw new Error(errorMsg);
            }
            return data;
        }).catch(error => {
            console.error('Response parsing error:', error);
            throw error;
        });
    }
}

// =====================================================================
// --- FILE ICON & COLOR HELPERS ---
// =====================================================================

export function getIconForFile(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const icons = {
        'blend': 'bi-box-fill', 'blend1': 'bi-box-fill',
        'pdf': 'bi-file-earmark-pdf-fill',
        'doc': 'bi-file-earmark-word-fill', 'docx': 'bi-file-earmark-word-fill',
        'xls': 'bi-file-earmark-excel-fill', 'xlsx': 'bi-file-earmark-excel-fill',
        'ppt': 'bi-file-earmark-slides-fill', 'pptx': 'bi-file-earmark-slides-fill',
        'txt': 'bi-file-earmark-text-fill', 'md': 'bi-file-earmark-text-fill',
        'jpg': 'bi-file-earmark-image-fill', 'jpeg': 'bi-file-earmark-image-fill',
        'png': 'bi-file-earmark-image-fill', 'gif': 'bi-file-earmark-image-fill',
        'zip': 'bi-file-earmark-zip-fill', 'rar': 'bi-file-earmark-zip-fill',
        'mp3': 'bi-file-earmark-music-fill', 'wav': 'bi-file-earmark-music-fill',
        'mp4': 'bi-file-earmark-play-fill', 'avi': 'bi-file-earmark-play-fill',
        'json': 'bi-file-earmark-code-fill', 'js': 'bi-file-earmark-code-fill',
        'py': 'bi-file-earmark-code-fill', 'html': 'bi-file-earmark-code-fill',
        'appimage': 'bi-box2-fill'
    };
    return icons[ext] || 'bi-file-earmark-fill';
}

export function getColorForFile(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const colors = {
        'blend': 'text-amber-600', 'blend1': 'text-amber-600',
        'pdf': 'text-red-500',
        'doc': 'text-blue-500', 'docx': 'text-blue-500',
        'xls': 'text-emerald-600', 'xlsx': 'text-emerald-600',
        'ppt': 'text-orange-500', 'pptx': 'text-orange-500',
        'jpg': 'text-pink-500', 'jpeg': 'text-pink-500', 'png': 'text-pink-500',
        'zip': 'text-purple-500', 'rar': 'text-purple-500',
        'mp3': 'text-purple-500', 'wav': 'text-purple-500',
        'mp4': 'text-red-500', 'avi': 'text-red-500',
        'json': 'text-orange-500', 'js': 'text-yellow-500',
        'py': 'text-blue-600', 'html': 'text-red-600',
        'appimage': 'text-cyan-400'
    };
    return colors[ext] || 'text-gray-500';
}

export function getFileIconDetails(filename) {
    if (typeof filename !== 'string' || !filename) {
        return { iconClass: 'bi bi-file-earmark-text-fill', iconColor: 'text-gray-500', thumbnail: null };
    }
    const ext = filename.split('.').pop().toLowerCase();
    let iconClass = 'bi bi-file-earmark-text-fill';
    let iconColor = 'text-gray-500';
    let thumbnail = null;

    if (ext === 'txt') {
        iconClass = 'bi bi-file-earmark-text-fill';
        iconColor = 'text-green-500';
    } else if (ext === 'blend') {
        iconClass = 'bi bi-box-fill-fill';
        iconColor = 'text-orange-500';
    } else if (['md', 'log', 'ini', 'config', 'cfg', 'conf', 'sh', 'py', 'js', 'html', 'css'].includes(ext)) {
        iconClass = 'bi bi-file-code-fill';
        iconColor = 'text-indigo-500';
    } else if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(ext)) {
        iconClass = 'bi bi-file-earmark-image-fill';
        iconColor = 'text-purple-500';
        thumbnail = `/static/data/images/${ext}.png`;
    } else if (['zip', 'rar', '7z', 'tar', 'gz'].includes(ext)) {
        iconClass = 'bi bi-file-earmark-zip-fill';
        iconColor = 'text-blue-500';
    } else if (['mp4', 'avi', 'mov', 'mkv'].includes(ext)) {
        iconClass = 'bi bi-file-earmark-play-fill';
        iconColor = 'text-red-500';
    } else if (['mp3', 'wav', 'flac', 'aac'].includes(ext)) {
        iconClass = 'bi bi-file-earmark-music-fill';
        iconColor = 'text-blue-500';
    } else if (['usb', 'vnmw', 'sd', 'mmc', 'sd-card', 'hd', 'memory', 'ext4'].includes(ext)) {
        iconClass = 'bi bi-device-hdd-fill';
        iconColor = 'text-green-500';
    }
    return { iconClass, iconColor, thumbnail };
}

// =====================================================================
// --- TIME FORMATTING ---
// =====================================================================

export function timeSince(timestamp) {
    const ts = typeof timestamp === 'number' ? timestamp : parseInt(timestamp);
    const timestampMs = ts < 10000000000 ? ts * 1000 : ts;
    const now = Date.now();
    const secondsAgo = Math.floor((now - timestampMs) / 1000);

    if (secondsAgo < 0) return 'just now';
    if (secondsAgo === 0) return 'just now';
    if (secondsAgo < 60) return `${secondsAgo} second${secondsAgo !== 1 ? 's' : ''} ago`;

    const minutesAgo = Math.floor(secondsAgo / 60);
    if (minutesAgo < 60) return `${minutesAgo} minute${minutesAgo !== 1 ? 's' : ''} ago`;

    const hoursAgo = Math.floor(minutesAgo / 60);
    if (hoursAgo < 24) return `${hoursAgo} hour${hoursAgo !== 1 ? 's' : ''} ago`;

    const daysAgo = Math.floor(hoursAgo / 24);
    if (daysAgo < 7) return `${daysAgo} day${daysAgo !== 1 ? 's' : ''} ago`;

    const weeksAgo = Math.floor(daysAgo / 7);
    if (weeksAgo < 4) return `${weeksAgo} week${weeksAgo !== 1 ? 's' : ''} ago`;

    const monthsAgo = Math.floor(daysAgo / 30);
    return `${monthsAgo} month${monthsAgo !== 1 ? 's' : ''} ago`;
}

export function humanFileSize(size) {
    const i = size == 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024));
    return (
        +(size / Math.pow(1024, i)).toFixed(2) * 1 +
        " " +
        ["B", "kB", "MB", "GB", "TB"][i]
    );
}

export function formatRelativeDate(dateString) {
    if (!dateString) return 'Unknown Date';

    const cleanedString = dateString.trim().replace(/[\s\.:]/g, '-');
    const parts = cleanedString.split('-').filter(p => p.length > 0);

    if (parts.length < 5) return dateString;

    let day, month, year, hour, minute;
    const h = Number(parts[3]);
    const m = Number(parts[4]);

    if (parts[0].length === 4) {
        [year, month, day] = parts.slice(0, 3).map(Number);
        [hour, minute] = [h, m];
    } else {
        const d1 = Number(parts[0]);
        const d2 = Number(parts[1]);
        const y = Number(parts[2]);

        if (d1 > 12) {
            [day, month, year, hour, minute] = [d1, d2, y, h, m];
        } else if (d2 > 12) {
            [day, month, year, hour, minute] = [d2, d1, y, h, m];
        } else {
            [day, month, year, hour, minute] = [d1, d2, y, h, m];
        }
    }

    const backupDate = new Date(year, month - 1, day, hour, minute);
    const now = new Date();

    const startOfBackupDay = new Date(backupDate.getFullYear(), backupDate.getMonth(), backupDate.getDate()).getTime();
    const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();

    const msPerDay = 1000 * 60 * 60 * 24;
    const dayDiffMs = startOfToday - startOfBackupDay;
    const diffDays = Math.floor(dayDiffMs / msPerDay);

    const formattedHours = String(backupDate.getHours()).padStart(2, '0');
    const formattedMinutes = String(backupDate.getMinutes()).padStart(2, '0');
    const time24H = `${formattedHours}:${formattedMinutes}`;

    if (diffDays === 0) return `Today, ${time24H}`;
    if (diffDays === 1) return `Yesterday, ${time24H}`;

    const formattedMonth = String(month).padStart(2, '0');
    const formattedDay = String(day).padStart(2, '0');

    return `${formattedDay}/${formattedMonth}/${year}, ${time24H}`;
}

export const formatBytes = Utils.formatBytes;

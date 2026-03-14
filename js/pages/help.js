// src/js/pages/help.js - FIXED

export default class HelpPage {
    constructor() {
        this.name = 'help';
    }

    async render() {
        return `
            <div class="px-8 py-6 flex items-end justify-between border-b border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark">
                <div>
                    <h1 class="text-2xl font-bold text-[var(--color-text-primary)] dark:text-white leading-tight">Help & Support</h1>
                    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">Get help with Backup Dashboard and find support resources.</p>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)] dark:bg-surface-dark p-8">
                <div class="max-w-4xl mx-auto">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="bg-gradient-to-br from-[var(--color-gray-50)] to-[var(--color-gray-100)] dark:from-[var(--color-gray-900)]/20 dark:to-[var(--color-gray-800)]/10 rounded-xl p-6 border border-[var(--color-gray-100)] dark:border-[var(--color-gray-700)]/30">
                            <div class="w-12 h-12 rounded-lg bg-[var(--color-accent)] flex items-center justify-center mb-4">
                                <span class="material-icons-round text-white text-2xl">description</span>
                            </div>
                            <h3 class="text-lg font-semibold text-[var(--color-text-primary)] dark:text-white mb-2">Documentation</h3>
                            <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mb-4">Read our comprehensive guides and tutorials.</p>
                            <button class="text-[var(--color-accent)] dark:text-[var(--color-accent)] font-medium hover:text-[var(--color-accent)] dark:hover:text-[var(--color-accent)] open-section-btn" data-section="documentation">
                                View Documentation →
                            </button>
                        </div>
                        
                        <div class="bg-gradient-to-br from-[var(--color-gray-50)] to-[var(--color-gray-100)] dark:from-[var(--color-gray-900)]/20 dark:to-[var(--color-gray-800)]/10 rounded-xl p-6 border border-[var(--color-status-success-bg)] dark:border-[var(--color-status-success-dark)]/30">
                            <div class="w-12 h-12 rounded-lg bg-[var(--color-status-success)] flex items-center justify-center mb-4">
                                <span class="material-icons-round text-white text-2xl">forum</span>
                            </div>
                            <h3 class="text-lg font-semibold text-[var(--color-text-primary)] dark:text-white mb-2">Community Forum</h3>
                            <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mb-4">Connect with other users and get help.</p>
                            <button class="text-[var(--color-status-success)] dark:text-[var(--color-status-success-dark)] font-medium hover:text-[var(--color-status-success)] dark:hover:text-[var(--color-status-success-dark)] open-section-btn" data-section="forum">
                                Visit Forum →
                            </button>
                        </div>
    
                    </div>
                    
                    <div class="mt-8 bg-[var(--color-gray-50)] dark:bg-[var(--color-gray-800)] rounded-xl p-6">
                        <h2 class="text-xl font-bold text-[var(--color-text-primary)] dark:text-white mb-4">Frequently Asked Questions</h2>
                        <div class="space-y-4">
                            <div class="border-b border-[var(--color-gray-200)] dark:border-[var(--color-gray-700)] pb-4">
                                <h3 class="font-medium text-[var(--color-text-primary)] dark:text-white mb-2">How often should I backup my files?</h3>
                                <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Time Machine backs up your files automatically and continuously — no manual scheduling needed. New and changed files are tracked in near real-time so your data is protected without extra effort.</p>
                            </div>
                            <div class="border-b border-[var(--color-gray-200)] dark:border-[var(--color-gray-700)] pb-4">
                                <h3 class="font-medium text-[var(--color-text-primary)] dark:text-white mb-2">How do I get versions of files from a backup?</h3>
                                <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Go to Files, select the file you want, then click "Get Versions". Choose the version you want from the list and restore or download it. If you need multiple versions, select the file and open the Versions window to browse history and restore any snapshot.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    afterRender() {
        console.log('Help page initialized');
        
        // Add event listeners to section buttons
        const sectionButtons = document.querySelectorAll('.open-section-btn');
        sectionButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const section = e.target.getAttribute('data-section');
                this.openSection(section);
            });
        });
    }

    openSection(section) {
        // Real URLs for documentation and forum
        const urls = {
            documentation: 'https://github.com/GeovaneJefferson/timemachine#readme',
            forum: 'https://github.com/GeovaneJefferson/timemachine/issues'
        };
        const url = urls[section];
        if (url) {
            window.open(url, '_blank');
        } else {
            console.warn('No URL defined for section', section);
        }
    }

    destroy() {
        console.log('Cleaning up Help page');
    }
}


// <div class="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/10 rounded-xl p-6 border border-[var(--color-gray-100)] dark:border-purple-800/30">
//     <div class="w-12 h-12 rounded-lg bg-[var(--color-gray-50)]0 flex items-center justify-center mb-4">
//         <span class="material-icons-round text-white text-2xl">contact_support</span>
//     </div>
//     <h3 class="text-lg font-semibold text-[var(--color-text-primary)] dark:text-white mb-2">Contact Support</h3>
//     <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mb-4">Get in touch with our support team.</p>
//     <button class="text-purple-600 dark:text-purple-400 font-medium hover:text-purple-700 dark:hover:text-purple-300 open-section-btn" data-section="contact">
//         Contact Us →
//     </button>
// </div>

// <div class="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-800/10 rounded-xl p-6 border border-[var(--color-gray-100)] dark:border-orange-800/30">
//     <div class="w-12 h-12 rounded-lg bg-[var(--color-gray-50)]0 flex items-center justify-center mb-4">
//         <span class="material-icons-round text-white text-2xl">video_library</span>
//     </div>
//     <h3 class="text-lg font-semibold text-[var(--color-text-primary)] dark:text-white mb-2">Video Tutorials</h3>
//     <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mb-4">Watch step-by-step video guides.</p>
//     <button class="text-orange-500 dark:text-orange-400 font-medium hover:text-orange-500 dark:hover:text-orange-300 open-section-btn" data-section="videos">
//         Watch Videos →
//     </button>
// </div>
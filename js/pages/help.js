// src/js/pages/help.js - FIXED

export default class HelpPage {
    constructor() {
        this.name = 'help';
    }

    async render() {
        return `
            <div class="px-8 py-6 flex items-end justify-between border-b border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900 dark:text-white leading-tight">Help & Support</h1>
                    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">Get help with Backup Dashboard and find support resources.</p>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark p-8">
                <div class="max-w-4xl mx-auto">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/10 rounded-xl p-6 border border-blue-100 dark:border-blue-800/30">
                            <div class="w-12 h-12 rounded-lg bg-blue-500 flex items-center justify-center mb-4">
                                <span class="material-icons-round text-white text-2xl">description</span>
                            </div>
                            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Documentation</h3>
                            <p class="text-gray-600 dark:text-gray-400 mb-4">Read our comprehensive guides and tutorials.</p>
                            <button class="text-blue-600 dark:text-blue-400 font-medium hover:text-blue-700 dark:hover:text-blue-300 open-section-btn" data-section="documentation">
                                View Documentation →
                            </button>
                        </div>
                        
                        <div class="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/10 rounded-xl p-6 border border-green-100 dark:border-green-800/30">
                            <div class="w-12 h-12 rounded-lg bg-green-500 flex items-center justify-center mb-4">
                                <span class="material-icons-round text-white text-2xl">forum</span>
                            </div>
                            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Community Forum</h3>
                            <p class="text-gray-600 dark:text-gray-400 mb-4">Connect with other users and get help.</p>
                            <button class="text-green-600 dark:text-green-400 font-medium hover:text-green-700 dark:hover:text-green-300 open-section-btn" data-section="forum">
                                Visit Forum →
                            </button>
                        </div>
    
                    </div>
                    
                    <div class="mt-8 bg-gray-50 dark:bg-gray-800 rounded-xl p-6">
                        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Frequently Asked Questions</h2>
                        <div class="space-y-4">
                            <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
                                <h3 class="font-medium text-gray-900 dark:text-white mb-2">How often should I backup my files?</h3>
                                <p class="text-gray-600 dark:text-gray-400">We recommend backing up important files daily, and performing full system backups weekly.</p>
                            </div>
                            <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
                                <h3 class="font-medium text-gray-900 dark:text-white mb-2">Can I backup to multiple locations?</h3>
                                <p class="text-gray-600 dark:text-gray-400">Yes, you can configure multiple backup destinations including local drives and cloud storage.</p>
                            </div>
                            <div class="border-b border-gray-200 dark:border-gray-700 pb-4">
                                <h3 class="font-medium text-gray-900 dark:text-white mb-2">How do I restore files from a backup?</h3>
                                <p class="text-gray-600 dark:text-gray-400">Navigate to the Files section, select the files you want to restore, and click the Restore button.</p>
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
        console.log(`Opening: ${section}`);
        
        const sectionTitles = {
            documentation: 'Documentation',
            forum: 'Community Forum',
            contact: 'Contact Support',
            videos: 'Video Tutorials'
        };
        
        const title = sectionTitles[section] || section;
        alert(`This would open the ${title} section in a real application.`);
    }

    destroy() {
        console.log('Cleaning up Help page');
    }
}


// <div class="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/10 rounded-xl p-6 border border-purple-100 dark:border-purple-800/30">
//     <div class="w-12 h-12 rounded-lg bg-purple-500 flex items-center justify-center mb-4">
//         <span class="material-icons-round text-white text-2xl">contact_support</span>
//     </div>
//     <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Contact Support</h3>
//     <p class="text-gray-600 dark:text-gray-400 mb-4">Get in touch with our support team.</p>
//     <button class="text-purple-600 dark:text-purple-400 font-medium hover:text-purple-700 dark:hover:text-purple-300 open-section-btn" data-section="contact">
//         Contact Us →
//     </button>
// </div>

// <div class="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-800/10 rounded-xl p-6 border border-orange-100 dark:border-orange-800/30">
//     <div class="w-12 h-12 rounded-lg bg-orange-500 flex items-center justify-center mb-4">
//         <span class="material-icons-round text-white text-2xl">video_library</span>
//     </div>
//     <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Video Tutorials</h3>
//     <p class="text-gray-600 dark:text-gray-400 mb-4">Watch step-by-step video guides.</p>
//     <button class="text-orange-600 dark:text-orange-400 font-medium hover:text-orange-700 dark:hover:text-orange-300 open-section-btn" data-section="videos">
//         Watch Videos →
//     </button>
// </div>
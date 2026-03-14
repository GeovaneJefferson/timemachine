// Loading Skeleton Utility - Reusable across all pages

export function createLoadingSkeleton(rows = 5, columns = 1) {
    return `
        <div class="animate-pulse space-y-4 p-6">
            ${[...Array(rows)].map(() => `
                <div class="space-y-3">
                    ${[...Array(columns)].map(() => `
                        <div class="h-4 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded w-full"></div>
                    `).join('')}
                </div>
            `).join('')}
        </div>
    `;
}

export function createTableLoadingSkeleton(rows = 5) {
    return `
        <div class="divide-y divide-gray-100 dark:divide-gray-800">
            ${[...Array(rows)].map(() => `
                <div class="px-6 py-4 flex gap-4 animate-pulse">
                    <div class="h-4 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded w-1/4"></div>
                    <div class="h-4 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded w-1/4"></div>
                    <div class="h-4 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded w-1/4"></div>
                    <div class="h-4 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded w-1/4"></div>
                </div>
            `).join('')}
        </div>
    `;
}

export function createCardLoadingSkeleton(count = 4) {
    return `
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            ${[...Array(count)].map(() => `
                <div class="bg-[var(--color-gray-100)] dark:bg-[var(--color-gray-800)] rounded-lg p-4 animate-pulse">
                    <div class="h-6 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded mb-3 w-3/4"></div>
                    <div class="h-4 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded w-full mb-2"></div>
                    <div class="h-4 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded w-2/3"></div>
                </div>
            `).join('')}
        </div>
    `;
}

export function createListLoadingSkeleton(items = 6) {
    return `
        <div class="space-y-2">
            ${[...Array(items)].map(() => `
                <div class="flex items-center gap-3 p-3 animate-pulse">
                    <div class="w-10 h-10 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded"></div>
                    <div class="flex-1 space-y-2">
                        <div class="h-4 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded w-3/4"></div>
                        <div class="h-3 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded w-1/2"></div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

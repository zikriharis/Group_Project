/* Dashboard JavaScript - Interactive functionality for the dashboard interface */

// Dashboard Main Object
const Dashboard = {
    // Initialize dashboard functionality
    init() {
        this.initTabs();
        this.initModals();
        this.initFilters();
        this.initSearch();
        this.initSorting();
        this.initBookmarks();
        this.initNotifications();
        this.initCharts();
        this.initForms();
        this.initTooltips();
        this.initMobileMenu();
        this.initRealTimeUpdates();
    },

    // Tab Navigation
    initTabs() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const targetTab = button.getAttribute('data-tab');

                // Remove active from all tabs and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));

                // Add active to clicked tab and corresponding content
                button.classList.add('active');
                const targetContent = document.getElementById(targetTab);
                if (targetContent) {
                    targetContent.classList.add('active');
                }

                // Update URL without reload
                history.pushState(null, null, `#${targetTab}`);
            });
        });

        // Handle initial tab from URL hash
        const hash = window.location.hash.substring(1);
        if (hash) {
            const targetButton = document.querySelector(`[data-tab="${hash}"]`);
            if (targetButton) {
                targetButton.click();
            }
        }
    },

    // Modal Management
    initModals() {
        // Modal triggers
        document.addEventListener('click', (e) => {
            // Open modal
            if (e.target.matches('[data-modal]')) {
                e.preventDefault();
                const modalId = e.target.getAttribute('data-modal');
                this.openModal(modalId);
            }

            // Close modal
            if (e.target.matches('.modal-close') || e.target.matches('.modal-overlay')) {
                this.closeModal();
            }
        });

        // Close modal with ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });
    },

    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    },

    closeModal() {
        const activeModal = document.querySelector('.modal.active');
        if (activeModal) {
            activeModal.classList.remove('active');
            document.body.style.overflow = '';
        }
    },

    // Filter Functionality
    initFilters() {
        const filterSelects = document.querySelectorAll('.filter-select');
        const filterButtons = document.querySelectorAll('.filter-btn');

        filterSelects.forEach(select => {
            select.addEventListener('change', () => {
                this.applyFilters();
            });
        });

        filterButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                button.classList.toggle('active');
                this.applyFilters();
            });
        });

        // Clear filters
        const clearFiltersBtn = document.querySelector('.clear-filters');
        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.clearFilters();
            });
        }
    },

    applyFilters() {
        const items = document.querySelectorAll('.filterable-item');
        const activeFilters = this.getActiveFilters();

        items.forEach(item => {
            let showItem = true;

            // Check each filter
            for (const [filterType, filterValue] of Object.entries(activeFilters)) {
                if (filterValue && filterValue !== 'all') {
                    const itemValue = item.getAttribute(`data-${filterType}`);
                    if (itemValue !== filterValue) {
                        showItem = false;
                        break;
                    }
                }
            }

            // Show/hide item
            item.style.display = showItem ? 'block' : 'none';
        });

        this.updateResultsCount();
    },

    getActiveFilters() {
        const filters = {};
        const filterSelects = document.querySelectorAll('.filter-select');

        filterSelects.forEach(select => {
            const filterType = select.getAttribute('data-filter');
            filters[filterType] = select.value;
        });

        return filters;
    },

    clearFilters() {
        const filterSelects = document.querySelectorAll('.filter-select');
        const filterButtons = document.querySelectorAll('.filter-btn.active');

        filterSelects.forEach(select => {
            select.value = 'all';
        });

        filterButtons.forEach(button => {
            button.classList.remove('active');
        });

        this.applyFilters();
    },

    // Search Functionality
    initSearch() {
        const searchInputs = document.querySelectorAll('.search-input');

        searchInputs.forEach(input => {
            let timeout;
            input.addEventListener('input', (e) => {
                clearTimeout(timeout);
                timeout = setTimeout(() => {
                    this.performSearch(e.target.value);
                }, 300);
            });
        });
    },

    performSearch(query) {
        const items = document.querySelectorAll('.searchable-item');
        const searchQuery = query.toLowerCase().trim();

        items.forEach(item => {
            const searchableText = item.getAttribute('data-search') || item.textContent;
            const isMatch = searchableText.toLowerCase().includes(searchQuery);
            item.style.display = isMatch ? 'block' : 'none';
        });

        this.updateResultsCount();
    },

    // Sorting Functionality
    initSorting() {
        const sortSelects = document.querySelectorAll('.sort-select');

        sortSelects.forEach(select => {
            select.addEventListener('change', (e) => {
                this.sortItems(e.target.value);
            });
        });
    },

    sortItems(sortBy) {
        const container = document.querySelector('.sortable-container');
        const items = Array.from(container.children);

        items.sort((a, b) => {
            const aValue = this.getSortValue(a, sortBy);
            const bValue = this.getSortValue(b, sortBy);

            if (sortBy.includes('date')) {
                return new Date(bValue) - new Date(aValue); // Newest first
            } else if (sortBy.includes('amount')) {
                return parseFloat(bValue) - parseFloat(aValue); // Highest first
            } else {
                return aValue.localeCompare(bValue); // Alphabetical
            }
        });

        // Re-append sorted items
        items.forEach(item => container.appendChild(item));
    },

    getSortValue(element, sortBy) {
        return element.getAttribute(`data-${sortBy}`) || '';
    },

    // Bookmark Management
    initBookmarks() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('.bookmark-btn') || e.target.closest('.bookmark-btn')) {
                e.preventDefault();
                const btn = e.target.closest('.bookmark-btn');
                const campaignId = btn.getAttribute('data-campaign-id');
                this.toggleBookmark(campaignId, btn);
            }

            if (e.target.matches('.share-btn')) {
                e.preventDefault();
                const campaignId = e.target.getAttribute('data-campaign-id');
                this.shareCampaign(campaignId);
            }
        });
    },

    async toggleBookmark(campaignId, button) {
        try {
            const response = await fetch(`/api/bookmarks/toggle/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ campaign_id: campaignId })
            });

            const data = await response.json();
            
            if (data.success) {
                button.classList.toggle('bookmarked', data.is_bookmarked);
                const icon = button.querySelector('i');
                if (icon) {
                    icon.className = data.is_bookmarked ? 'fas fa-bookmark' : 'far fa-bookmark';
                }
                this.showToast(data.message);
            }
        } catch (error) {
            console.error('Bookmark error:', error);
            this.showToast('Error updating bookmark', 'error');
        }
    },

    shareCampaign(campaignId) {
        const url = `${window.location.origin}/campaigns/${campaignId}/`;
        
        if (navigator.share) {
            navigator.share({
                title: 'Check out this campaign',
                url: url
            });
        } else {
            // Fallback: copy to clipboard
            navigator.clipboard.writeText(url).then(() => {
                this.showToast('Campaign link copied to clipboard!');
            });
        }
    },

    // Notifications Management
    initNotifications() {
        document.addEventListener('click', (e) => {
            if (e.target.matches('.mark-read-btn')) {
                e.preventDefault();
                const notificationId = e.target.getAttribute('data-notification-id');
                this.markNotificationRead(notificationId);
            }

            if (e.target.matches('.mark-all-read-btn')) {
                e.preventDefault();
                this.markAllNotificationsRead();
            }

            if (e.target.matches('.delete-notification-btn')) {
                e.preventDefault();
                const notificationId = e.target.getAttribute('data-notification-id');
                this.deleteNotification(notificationId);
            }
        });

        // Auto-refresh notifications
        setInterval(() => {
            this.checkNewNotifications();
        }, 30000); // Check every 30 seconds
    },

    async markNotificationRead(notificationId) {
        try {
            const response = await fetch(`/api/notifications/${notificationId}/read/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                const notification = document.querySelector(`[data-notification-id="${notificationId}"]`);
                if (notification) {
                    notification.classList.remove('unread');
                }
                this.updateNotificationBadge();
            }
        } catch (error) {
            console.error('Mark read error:', error);
        }
    },

    async markAllNotificationsRead() {
        try {
            const response = await fetch('/api/notifications/mark-all-read/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                document.querySelectorAll('.notification-item.unread').forEach(item => {
                    item.classList.remove('unread');
                });
                this.updateNotificationBadge();
                this.showToast('All notifications marked as read');
            }
        } catch (error) {
            console.error('Mark all read error:', error);
        }
    },

    async deleteNotification(notificationId) {
        if (!confirm('Are you sure you want to delete this notification?')) {
            return;
        }

        try {
            const response = await fetch(`/api/notifications/${notificationId}/delete/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                const notification = document.querySelector(`[data-notification-id="${notificationId}"]`);
                if (notification) {
                    notification.remove();
                }
                this.updateNotificationBadge();
                this.showToast('Notification deleted');
            }
        } catch (error) {
            console.error('Delete notification error:', error);
        }
    },

    async checkNewNotifications() {
        try {
            const response = await fetch('/api/notifications/unread-count/');
            const data = await response.json();
            this.updateNotificationBadge(data.count);
        } catch (error) {
            console.error('Check notifications error:', error);
        }
    },

    updateNotificationBadge(count = null) {
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            if (count === null) {
                count = document.querySelectorAll('.notification-item.unread').length;
            }
            badge.textContent = count;
            badge.style.display = count > 0 ? 'block' : 'none';
        }
    },

    // Charts Initialization
    initCharts() {
        this.initStatisticCounters();
        this.initProgressBars();
        this.initRealTimeCharts();
    },

    // Animated statistic counters
    initStatisticCounters() {
        const statCards = document.querySelectorAll('.stat-card');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const statContent = entry.target.querySelector('.stat-content h3');
                    if (statContent && !statContent.hasAttribute('data-animated')) {
                        this.animateCounter(statContent);
                        statContent.setAttribute('data-animated', 'true');
                    }
                }
            });
        }, { threshold: 0.5 });

        statCards.forEach(card => observer.observe(card));
    },

    animateCounter(element) {
        const target = parseFloat(element.textContent.replace(/[$,]/g, ''));
        const isMonetary = element.textContent.includes('$');
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            let displayValue = Math.floor(current);
            if (isMonetary) {
                displayValue = '$' + displayValue.toLocaleString();
            } else {
                displayValue = displayValue.toLocaleString();
            }
            element.textContent = displayValue;
        }, 16);
    },

    // Animate progress bars
    initProgressBars() {
        const progressBars = document.querySelectorAll('.progress-fill');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBar = entry.target;
                    const targetWidth = progressBar.style.width;
                    progressBar.style.width = '0%';
                    progressBar.style.transition = 'width 1.5s ease-out';
                    
                    setTimeout(() => {
                        progressBar.style.width = targetWidth;
                    }, 200);
                }
            });
        }, { threshold: 0.5 });

        progressBars.forEach(bar => observer.observe(bar));
    },

    // Real-time chart updates
    initRealTimeCharts() {
        // Check for real-time updates every 5 minutes
        setInterval(() => {
            this.updateDashboardData();
        }, 300000);
    },

    async updateDashboardData() {
        try {
            const response = await fetch('/dashboard/api/real-time-data/');
            if (response.ok) {
                const data = await response.json();
                this.updateStatCards(data);
                this.updateCharts(data);
            }
        } catch (error) {
            console.log('Failed to fetch real-time data:', error);
        }
    },

    updateStatCards(data) {
        // Update stat cards with new data
        Object.keys(data.stats || {}).forEach(statKey => {
            const statElement = document.querySelector(`[data-stat="${statKey}"]`);
            if (statElement) {
                this.animateCounter(statElement);
            }
        });
    },

    updateCharts(data) {
        // Update Chart.js charts with new data
        if (window.dashboardCharts) {
            Object.keys(window.dashboardCharts).forEach(chartKey => {
                const chart = window.dashboardCharts[chartKey];
                if (data.charts && data.charts[chartKey]) {
                    chart.data = data.charts[chartKey];
                    chart.update('none');
                }
            });
        }
    },

    // Form Handling
    initForms() {
        const forms = document.querySelectorAll('.ajax-form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.submitForm(form);
            });
        });

        // File upload preview
        const fileInputs = document.querySelectorAll('input[type="file"]');
        fileInputs.forEach(input => {
            input.addEventListener('change', (e) => {
                this.previewFile(e.target);
            });
        });
    },

    async submitForm(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';

        try {
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            const data = await response.json();
            
            if (data.success) {
                this.showToast(data.message || 'Form submitted successfully!');
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    form.reset();
                    this.closeModal();
                }
            } else {
                this.showToast(data.message || 'Form submission failed', 'error');
                this.displayFormErrors(form, data.errors);
            }
        } catch (error) {
            console.error('Form submission error:', error);
            this.showToast('An error occurred while submitting the form', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    },

    displayFormErrors(form, errors) {
        // Clear previous errors
        form.querySelectorAll('.error-message').forEach(error => error.remove());
        form.querySelectorAll('.error').forEach(field => field.classList.remove('error'));

        // Display new errors
        for (const [field, messages] of Object.entries(errors)) {
            const fieldElement = form.querySelector(`[name="${field}"]`);
            if (fieldElement) {
                fieldElement.classList.add('error');
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-message';
                errorDiv.textContent = messages[0];
                fieldElement.parentNode.appendChild(errorDiv);
            }
        }
    },

    previewFile(input) {
        const file = input.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const preview = input.parentNode.querySelector('.file-preview');
                if (preview) {
                    if (file.type.startsWith('image/')) {
                        preview.innerHTML = `<img src="${e.target.result}" alt="Preview" style="max-width: 200px; max-height: 200px;">`;
                    } else {
                        preview.innerHTML = `<p>File selected: ${file.name}</p>`;
                    }
                }
            };
            reader.readAsDataURL(file);
        }
    },

    // Tooltips
    initTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                this.showTooltip(e.target);
            });

            element.addEventListener('mouseleave', () => {
                this.hideTooltip();
            });
        });
    },

    showTooltip(element) {
        const text = element.getAttribute('data-tooltip');
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = text;
        document.body.appendChild(tooltip);

        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
        tooltip.style.opacity = '1';
    },

    hideTooltip() {
        const tooltip = document.querySelector('.tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    },

    // Mobile Menu
    initMobileMenu() {
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        const sideNav = document.querySelector('.dashboard-sidebar');
        const overlay = document.querySelector('.mobile-overlay');

        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', () => {
                sideNav.classList.toggle('active');
                overlay.classList.toggle('active');
            });
        }

        if (overlay) {
            overlay.addEventListener('click', () => {
                sideNav.classList.remove('active');
                overlay.classList.remove('active');
            });
        }
    },

    // Real-time Updates
    initRealTimeUpdates() {
        // Check for updates every 60 seconds
        setInterval(() => {
            this.checkForUpdates();
        }, 60000);
    },

    async checkForUpdates() {
        try {
            const response = await fetch('/api/dashboard/updates/');
            const data = await response.json();
            
            if (data.has_updates) {
                this.showUpdateNotification();
            }
        } catch (error) {
            console.error('Update check error:', error);
        }
    },

    showUpdateNotification() {
        const notification = document.createElement('div');
        notification.className = 'update-notification';
        notification.innerHTML = `
            <div class="update-content">
                <i class="fas fa-refresh"></i>
                <span>New data available</span>
                <button onclick="window.location.reload()">Refresh</button>
            </div>
        `;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
    },

    // Utility Functions
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    },

    showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${type === 'success' ? 'check' : 'exclamation-triangle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    updateResultsCount() {
        const visibleItems = document.querySelectorAll('.filterable-item[style*="block"], .searchable-item[style*="block"]');
        const countElement = document.querySelector('.results-count');
        if (countElement) {
            countElement.textContent = `${visibleItems.length} results`;
        }
    },

    // Format currency
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },

    // Format date
    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }
};

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    Dashboard.init();
});

// Export for use in other scripts
window.Dashboard = Dashboard;

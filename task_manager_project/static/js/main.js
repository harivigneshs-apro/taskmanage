// Main JavaScript for Task Manager

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('a[href*="delete"]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Task status quick update
    const statusButtons = document.querySelectorAll('.status-update-btn');
    statusButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const taskId = this.dataset.taskId;
            const status = this.dataset.status;
            updateTaskStatus(taskId, status);
        });
    });

    // Search functionality
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                // Auto-submit search form after 500ms of no typing
                const form = searchInput.closest('form');
                if (form) {
                    form.submit();
                }
            }, 500);
        });
    }

    // Priority color coding
    updatePriorityColors();
    
    // Status color coding
    updateStatusColors();

    // Initialize date/time pickers
    initializeDateTimePickers();

    // Task card hover effects
    addTaskCardEffects();
});

// Function to update task status via AJAX
function updateTaskStatus(taskId, status) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/tasks/${taskId}/toggle-status/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `status=${status}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the status badge
            const statusBadge = document.querySelector(`[data-task-id="${taskId}"] .status-badge`);
            if (statusBadge) {
                statusBadge.textContent = data.status;
                statusBadge.className = `badge bg-${status} status-badge`;
            }
            
            // Show success message
            showNotification('Task status updated successfully!', 'success');
        } else {
            showNotification('Failed to update task status.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred while updating the task.', 'error');
    });
}

// Function to show notifications
function showNotification(message, type = 'info') {
    const alertClass = type === 'error' ? 'alert-danger' : `alert-${type}`;
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Find or create notification container
    let container = document.querySelector('.notification-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'notification-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1050';
        document.body.appendChild(container);
    }
    
    container.insertAdjacentHTML('beforeend', alertHtml);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        const alert = container.lastElementChild;
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

// Function to update priority colors
function updatePriorityColors() {
    const priorityElements = document.querySelectorAll('[data-priority]');
    priorityElements.forEach(function(element) {
        const priority = element.dataset.priority;
        element.classList.add(`bg-${priority}`);
    });
}

// Function to update status colors
function updateStatusColors() {
    const statusElements = document.querySelectorAll('[data-status]');
    statusElements.forEach(function(element) {
        const status = element.dataset.status;
        element.classList.add(`bg-${status}`);
    });
}

// Function to initialize date/time pickers
function initializeDateTimePickers() {
    const dateTimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    dateTimeInputs.forEach(function(input) {
        // Set minimum date to current date/time
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        
        const minDateTime = `${year}-${month}-${day}T${hours}:${minutes}`;
        input.setAttribute('min', minDateTime);
    });
}

// Function to add task card effects
function addTaskCardEffects() {
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.classList.add('shadow-lg');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-lg');
        });
    });
}

// Function to handle form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Function to handle AJAX form submissions
function submitFormAjax(form, successCallback) {
    const formData = new FormData(form);
    const url = form.action || window.location.href;
    
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (successCallback) {
                successCallback(data);
            }
            showNotification(data.message || 'Operation completed successfully!', 'success');
        } else {
            showNotification(data.message || 'An error occurred.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An unexpected error occurred.', 'error');
    });
}

// Function to format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Function to calculate time remaining
function getTimeRemaining(dueDate) {
    const now = new Date();
    const due = new Date(dueDate);
    const diff = due - now;
    
    if (diff < 0) {
        return 'Overdue';
    }
    
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    
    if (days > 0) {
        return `${days} day${days > 1 ? 's' : ''} remaining`;
    } else if (hours > 0) {
        return `${hours} hour${hours > 1 ? 's' : ''} remaining`;
    } else {
        return 'Due soon';
    }
}

// Function to update time remaining displays
function updateTimeRemaining() {
    const timeElements = document.querySelectorAll('[data-due-date]');
    timeElements.forEach(function(element) {
        const dueDate = element.dataset.dueDate;
        const timeRemaining = getTimeRemaining(dueDate);
        element.textContent = timeRemaining;
        
        // Add appropriate classes based on time remaining
        if (timeRemaining === 'Overdue') {
            element.classList.add('text-danger');
        } else if (timeRemaining.includes('hour')) {
            element.classList.add('text-warning');
        } else {
            element.classList.add('text-success');
        }
    });
}

// Update time remaining every minute
setInterval(updateTimeRemaining, 60000);

// Export functions for use in other scripts
window.TaskManager = {
    updateTaskStatus,
    showNotification,
    validateForm,
    submitFormAjax,
    formatDate,
    getTimeRemaining
};

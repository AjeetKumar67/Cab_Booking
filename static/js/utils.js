// Utility Functions for the Cab Booking Application

// Show loading spinner
function showSpinner(message = "Loading...") {
    // Create spinner overlay if it doesn't exist
    if (!document.getElementById("spinner-overlay")) {
        const spinnerHTML = `
            <div id="spinner-overlay" class="spinner-overlay">
                <div class="spinner-container">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="mt-2" id="spinner-message">${message}</div>
                </div>
            </div>
        `;
        
        const spinnerElement = document.createElement("div");
        spinnerElement.innerHTML = spinnerHTML;
        document.body.appendChild(spinnerElement.firstElementChild);
    } else {
        // Update message if spinner already exists
        document.getElementById("spinner-message").textContent = message;
        document.getElementById("spinner-overlay").style.display = "flex";
    }
}

// Hide loading spinner
function hideSpinner() {
    const spinner = document.getElementById("spinner-overlay");
    if (spinner) {
        spinner.style.display = "none";
    }
}

// Format currency (Indian Rupees)
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 2
    }).format(amount);
}

// Format date and time
function formatDateTime(dateString) {
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

// Format just the date
function formatDate(dateString) {
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    };
    
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

// Calculate time difference in minutes
function getTimeDifference(startTime, endTime) {
    const start = new Date(startTime);
    const end = new Date(endTime);
    const diffMs = end - start;
    return Math.round(diffMs / 60000); // Convert to minutes
}

// Format time difference to human-readable form
function formatTimeDifference(minutes) {
    if (minutes < 60) {
        return `${minutes} min${minutes !== 1 ? 's' : ''}`;
    } else {
        const hours = Math.floor(minutes / 60);
        const remainingMinutes = minutes % 60;
        
        if (remainingMinutes === 0) {
            return `${hours} hr${hours !== 1 ? 's' : ''}`;
        } else {
            return `${hours} hr${hours !== 1 ? 's' : ''} ${remainingMinutes} min${remainingMinutes !== 1 ? 's' : ''}`;
        }
    }
}

// Get status badge class based on ride status
function getStatusBadgeClass(status) {
    const statusClasses = {
        'requested': 'bg-warning',
        'accepted': 'bg-info',
        'started': 'bg-primary',
        'completed': 'bg-success',
        'cancelled': 'bg-danger'
    };
    
    return statusClasses[status] || 'bg-secondary';
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Confirm dialog with promise
function confirmDialog(message) {
    return new Promise((resolve) => {
        if (confirm(message)) {
            resolve(true);
        } else {
            resolve(false);
        }
    });
}

// Copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => {
            // Show success message
            showAlert("Copied to clipboard!", "success");
        })
        .catch(err => {
            console.error("Failed to copy text: ", err);
            showAlert("Failed to copy to clipboard", "danger");
        });
}

// Show a toast notification
function showToast(message, type = "info") {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector(".toast-container");
    if (!toastContainer) {
        toastContainer = document.createElement("div");
        toastContainer.className = "toast-container position-fixed bottom-0 end-0 p-3";
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = `toast-${Date.now()}`;
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header bg-${type} text-white">
                <strong class="me-auto">Notification</strong>
                <small>Just now</small>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    // Append toast to container
    const toastElement = document.createElement("div");
    toastElement.innerHTML = toastHTML;
    toastContainer.appendChild(toastElement.firstElementChild);
    
    // Initialize and show the toast
    const toastInstance = new bootstrap.Toast(document.getElementById(toastId));
    toastInstance.show();
    
    // Remove toast after it's hidden
    document.getElementById(toastId).addEventListener('hidden.bs.toast', function () {
        this.remove();
    });
}

// Show alert message
function showAlert(message, type = "info") {
    const alertsContainer = document.getElementById("alerts-container");
    if (!alertsContainer) return;
    
    const alertDiv = document.createElement("div");
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = "alert";
    
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertsContainer.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.classList.remove("show");
        setTimeout(() => {
            alertDiv.remove();
        }, 150);
    }, 5000);
}

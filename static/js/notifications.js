// Notification and Real-time Updates

// Poll for new notifications every 30 seconds
const NOTIFICATION_POLL_INTERVAL = 30000;

document.addEventListener("DOMContentLoaded", function() {
    // Start polling for notifications
    setTimeout(updateNotificationCount, 1000);
    setInterval(updateNotificationCount, NOTIFICATION_POLL_INTERVAL);
    
    // Setup notification click handlers
    setupNotificationHandlers();
});

function updateNotificationCount() {
    fetch("/notifications/count/")
        .then(response => response.json())
        .then(data => {
            const count = data.count;
            const badge = document.getElementById("notification-badge");
            
            if (badge) {
                if (count > 0) {
                    badge.textContent = count;
                    badge.style.display = "inline";
                } else {
                    badge.style.display = "none";
                }
            }
        })
        .catch(error => console.error("Error fetching notification count:", error));
}

function setupNotificationHandlers() {
    // Mark notification as read when clicked
    document.querySelectorAll(".notification-item").forEach(item => {
        item.addEventListener("click", function() {
            const notificationId = this.dataset.notificationId;
            markNotificationAsRead(notificationId);
        });
    });
    
    // Mark all notifications as read
    const markAllReadBtn = document.getElementById("mark-all-read");
    if (markAllReadBtn) {
        markAllReadBtn.addEventListener("click", markAllNotificationsAsRead);
    }
}

function markNotificationAsRead(notificationId) {
    fetch(`/notifications/mark-read/${notificationId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Update UI to show notification as read
            const notification = document.querySelector(`.notification-item[data-notification-id="${notificationId}"]`);
            if (notification) {
                notification.classList.add("bg-light");
                notification.classList.remove("bg-light-hover");
            }
            
            // Update notification count
            updateNotificationCount();
        }
    })
    .catch(error => console.error("Error marking notification as read:", error));
}

function markAllNotificationsAsRead() {
    fetch("/notifications/mark-all-read/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Update UI to show all notifications as read
            document.querySelectorAll(".notification-item").forEach(item => {
                item.classList.add("bg-light");
                item.classList.remove("bg-light-hover");
            });
            
            // Update notification count
            updateNotificationCount();
        }
    })
    .catch(error => console.error("Error marking all notifications as read:", error));
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

// For Ride Updates (Driver Dashboard)
function checkForNewRideRequests() {
    // This would be replaced with WebSockets in a production app
    // For now, we're just refreshing the page to check for new rides
    fetch("/drivers/check-new-rides/")
        .then(response => response.json())
        .then(data => {
            if (data.has_new_rides) {
                // Play notification sound
                const audio = new Audio("/static/sounds/notification.mp3");
                audio.play();
                
                // Show notification
                if ("Notification" in window && Notification.permission === "granted") {
                    new Notification("New Ride Request", {
                        body: "You have a new ride request. Check your dashboard.",
                        icon: "/static/images/logo.png"
                    });
                }
                
                // Refresh the rides list
                refreshRidesList();
            }
        })
        .catch(error => console.error("Error checking for new rides:", error));
}

function refreshRidesList() {
    const ridesList = document.getElementById("rides-list");
    if (ridesList) {
        fetch("/rides/list-partial/")
            .then(response => response.text())
            .then(html => {
                ridesList.innerHTML = html;
            })
            .catch(error => console.error("Error refreshing rides list:", error));
    }
}

// Request notification permission
function requestNotificationPermission() {
    if ("Notification" in window) {
        Notification.requestPermission().then(function(permission) {
            if (permission === "granted") {
                console.log("Notification permission granted");
            }
        });
    }
}

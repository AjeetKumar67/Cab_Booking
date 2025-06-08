// Payment Handling

document.addEventListener("DOMContentLoaded", function() {
    // Setup payment method selection
    setupPaymentMethodSelection();
    
    // Setup rating stars functionality
    setupRatingStars();
});

function setupPaymentMethodSelection() {
    const paymentMethodRadios = document.querySelectorAll('input[name="payment_method"]');
    const paymentMethodUpdateBtn = document.getElementById("update-payment-method");
    
    if (paymentMethodRadios.length > 0 && paymentMethodUpdateBtn) {
        paymentMethodUpdateBtn.addEventListener("click", function() {
            const selectedMethod = document.querySelector('input[name="payment_method"]:checked');
            if (selectedMethod) {
                updatePaymentMethod(selectedMethod.value);
            }
        });
    }
}

function updatePaymentMethod(method) {
    const paymentId = document.getElementById("payment-id").value;
    
    fetch(`/payments/update-payment-method/${paymentId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            payment_method: method
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Show success message
            showAlert("Payment method updated successfully", "success");
        } else {
            showAlert("Failed to update payment method", "danger");
        }
    })
    .catch(error => {
        console.error("Error updating payment method:", error);
        showAlert("An error occurred. Please try again.", "danger");
    });
}

function setupRatingStars() {
    const ratingStars = document.querySelectorAll(".rating-stars i");
    const ratingInput = document.getElementById("id_rating");
    
    if (ratingStars.length > 0 && ratingInput) {
        // Set initial rating if already selected
        const initialRating = parseInt(ratingInput.value, 10);
        if (initialRating > 0) {
            highlightStars(initialRating);
        }
        
        // Add click event to stars
        ratingStars.forEach((star, index) => {
            star.addEventListener("click", function() {
                const rating = index + 1;
                ratingInput.value = rating;
                highlightStars(rating);
            });
            
            // Add hover effect
            star.addEventListener("mouseenter", function() {
                const rating = index + 1;
                highlightStars(rating, true);
            });
            
            star.addEventListener("mouseleave", function() {
                const rating = parseInt(ratingInput.value, 10) || 0;
                highlightStars(rating);
            });
        });
    }
}

function highlightStars(rating, isHover = false) {
    const stars = document.querySelectorAll(".rating-stars i");
    
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add("active");
        } else {
            if (!isHover) {
                star.classList.remove("active");
            }
        }
    });
}

function showAlert(message, type) {
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

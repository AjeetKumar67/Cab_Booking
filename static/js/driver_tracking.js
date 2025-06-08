// Driver Location Tracking

let map;
let marker;
let watchId;
let isTracking = false;

function initDriverMap() {
    // Initialize the map centered at a default location
    map = new google.maps.Map(document.getElementById("driverMap"), {
        center: { lat: 28.6139, lng: 77.2090 }, // Default to Delhi, India
        zoom: 15,
    });
    
    // Create a marker for the driver's position
    marker = new google.maps.Marker({
        map: map,
        icon: {
            url: 'https://maps.google.com/mapfiles/ms/icons/green-dot.png',
            scaledSize: new google.maps.Size(40, 40)
        },
        title: "Your location"
    });
    
    // Check if geolocation is available
    if (navigator.geolocation) {
        // Get initial position
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };
                
                // Update map and marker
                map.setCenter(pos);
                marker.setPosition(pos);
                
                // Send initial location to server
                updateDriverLocation(pos.lat, pos.lng);
            },
            () => {
                handleLocationError(true);
            }
        );
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false);
    }
    
    // Add event listener to the toggle button
    document.getElementById("toggleTracking").addEventListener("click", toggleLocationTracking);
}

function toggleLocationTracking() {
    const toggleButton = document.getElementById("toggleTracking");
    
    if (isTracking) {
        // Stop tracking
        if (watchId) {
            navigator.geolocation.clearWatch(watchId);
            watchId = null;
        }
        
        toggleButton.textContent = "Start Tracking";
        toggleButton.classList.remove("btn-danger");
        toggleButton.classList.add("btn-success");
        
        isTracking = false;
    } else {
        // Start tracking
        if (navigator.geolocation) {
            watchId = navigator.geolocation.watchPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };
                    
                    // Update map and marker
                    map.setCenter(pos);
                    marker.setPosition(pos);
                    
                    // Send location to server
                    updateDriverLocation(pos.lat, pos.lng);
                },
                () => {
                    handleLocationError(true);
                },
                { enableHighAccuracy: true, maximumAge: 0, timeout: 5000 }
            );
        } else {
            handleLocationError(false);
            return;
        }
        
        toggleButton.textContent = "Stop Tracking";
        toggleButton.classList.remove("btn-success");
        toggleButton.classList.add("btn-danger");
        
        isTracking = true;
    }
}

function updateDriverLocation(latitude, longitude) {
    // Send location data to server using fetch API
    fetch("/drivers/update-location/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            latitude: latitude,
            longitude: longitude
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            console.log("Location updated successfully");
        } else {
            console.error("Failed to update location:", data.message);
        }
    })
    .catch(error => {
        console.error("Error updating location:", error);
    });
}

function handleLocationError(browserHasGeolocation) {
    console.error(
        browserHasGeolocation
        ? "Error: The Geolocation service failed."
        : "Error: Your browser doesn't support geolocation."
    );
    
    alert(
        browserHasGeolocation
        ? "Error: The Geolocation service failed. Please enable location services."
        : "Error: Your browser doesn't support geolocation."
    );
}

// Helper function to get CSRF token from cookies
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

// Google Maps Integration for Ride Booking

let map;
let directionsService;
let directionsRenderer;
let autocompletePickup;
let autocompleteDrop;

function initMap() {
    // Initialize the map
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 28.6139, lng: 77.2090 }, // Default to Delhi, India
        zoom: 12,
    });
    
    // Initialize directions service and renderer
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        draggable: true,
        hideRouteList: true,
    });
    
    // Initialize autocomplete for pickup and drop locations
    autocompletePickup = new google.maps.places.Autocomplete(
        document.getElementById("pickup-location"),
        { types: ["geocode"] }
    );
    
    autocompleteDrop = new google.maps.places.Autocomplete(
        document.getElementById("drop-location"),
        { types: ["geocode"] }
    );
    
    // Add listeners to autocomplete fields
    autocompletePickup.addListener("place_changed", function() {
        const place = autocompletePickup.getPlace();
        if (place.geometry) {
            document.getElementById("pickup-latitude").value = place.geometry.location.lat();
            document.getElementById("pickup-longitude").value = place.geometry.location.lng();
            calculateRoute();
        }
    });
    
    autocompleteDrop.addListener("place_changed", function() {
        const place = autocompleteDrop.getPlace();
        if (place.geometry) {
            document.getElementById("drop-latitude").value = place.geometry.location.lat();
            document.getElementById("drop-longitude").value = place.geometry.location.lng();
            calculateRoute();
        }
    });
}

function calculateRoute() {
    // Get pickup and drop coordinates
    const pickupLat = document.getElementById("pickup-latitude").value;
    const pickupLng = document.getElementById("pickup-longitude").value;
    const dropLat = document.getElementById("drop-latitude").value;
    const dropLng = document.getElementById("drop-longitude").value;
    
    // Check if all coordinates are available
    if (pickupLat && pickupLng && dropLat && dropLng) {
        const request = {
            origin: new google.maps.LatLng(pickupLat, pickupLng),
            destination: new google.maps.LatLng(dropLat, dropLng),
            travelMode: google.maps.TravelMode.DRIVING,
        };
        
        directionsService.route(request, function(result, status) {
            if (status === "OK") {
                directionsRenderer.setDirections(result);
                
                // Get distance and duration
                const route = result.routes[0];
                const leg = route.legs[0];
                
                // Set distance in the form
                const distanceInKm = leg.distance.value / 1000; // Convert meters to kilometers
                document.getElementById("distance").value = distanceInKm.toFixed(2);
                document.getElementById("displayDistance").textContent = `${distanceInKm.toFixed(2)} km`;
                
                // Set estimated time
                document.getElementById("estimatedTime").textContent = leg.duration.text;
                
                // Show fare estimate
                updateFareEstimate();
                document.querySelector(".fare-estimate").classList.remove("d-none");
            }
        });
    }
}

function updateFareEstimate() {
    // Get selected cab type
    const selectedCab = document.querySelector(".cab-option.selected");
    if (!selectedCab) return;
    
    const baseFare = parseFloat(selectedCab.dataset.baseFare);
    const pricePerKm = parseFloat(selectedCab.dataset.pricePerKm);
    const distance = parseFloat(document.getElementById("distance").value);
    
    // Calculate fare
    const distanceCharge = pricePerKm * distance;
    const totalFare = baseFare + distanceCharge;
    
    // Update fare display
    document.getElementById("baseFare").textContent = `₹${baseFare.toFixed(2)}`;
    document.getElementById("distanceCharge").textContent = `₹${distanceCharge.toFixed(2)}`;
    document.getElementById("totalFare").textContent = `₹${totalFare.toFixed(2)}`;
    
    // Update the hidden field for cab type
    const cabId = selectedCab.dataset.cabId;
    document.querySelector(`input[name="cab_type"][value="${cabId}"]`).checked = true;
}

// Event listeners for cab options
document.addEventListener("DOMContentLoaded", function() {
    const cabOptions = document.querySelectorAll(".cab-option");
    
    cabOptions.forEach(function(option) {
        option.addEventListener("click", function() {
            // Remove selected class from all options
            cabOptions.forEach(opt => opt.classList.remove("selected"));
            
            // Add selected class to clicked option
            this.classList.add("selected");
            
            // Update fare estimate
            updateFareEstimate();
        });
    });
    
    // Select the first cab option by default
    if (cabOptions.length > 0) {
        cabOptions[0].classList.add("selected");
    }
});

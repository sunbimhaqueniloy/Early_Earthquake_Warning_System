function simulateEarthquake() {
    const cities = ["Dhaka", "Chattogram", "Sylhet", "Rajshahi", "Khulna"];
    const city = cities[Math.floor(Math.random() * cities.length)];

    const magnitude = (Math.random() * 3 + 4).toFixed(1); // 4.0 to 7.0
    const distance = Math.floor(Math.random() * 120) + 30; // 30 to 150 km
    const waveSpeed = 5; // km/s
    const arrivalTime = Math.floor(distance / waveSpeed);

    let alertLevel = "";
    let infraActions = [];

    if (magnitude >= 6.5) {
        alertLevel = "HIGH";
        infraActions = [
            "Power Grid: Emergency shutdown initiated",
            "Gas System: Main valves closed",
            "Transport: Metro/train pause alert sent",
            "Hospitals: Emergency preparedness activated"
        ];
    } else if (magnitude >= 5.5) {
        alertLevel = "MEDIUM";
        infraActions = [
            "Power Grid: Monitoring voltage stability",
            "Gas System: Pressure warning issued",
            "Transport: Speed reduction alert",
            "Hospitals: Standby notification sent"
        ];
    } else {
        alertLevel = "LOW";
        infraActions = [
            "Infrastructure under observation",
            "No shutdown required",
            "Public advisory issued"
        ];
    }

    document.getElementById("statusText").innerHTML = "Status: 🚨 Earthquake detected!";
    document.getElementById("magnitudeText").innerHTML = `Magnitude: ${magnitude}`;
    document.getElementById("distanceText").innerHTML = `Distance: ${distance} km`;
    document.getElementById("cityText").innerHTML = `Target City: ${city}`;

    const alertText = document.getElementById("alertText");
    alertText.innerHTML = `Alert Level: ${alertLevel}`;

    if (alertLevel === "HIGH") {
        alertText.className = "info-line danger";
    } else if (alertLevel === "MEDIUM") {
        alertText.className = "info-line warning";
    } else {
        alertText.className = "info-line safe";
    }

    const infraList = document.getElementById("infraList");
    infraList.innerHTML = "";
    infraActions.forEach(action => {
        const li = document.createElement("li");
        li.textContent = action;
        infraList.appendChild(li);
    });

    showMapMarker();
    startCountdown(arrivalTime);
}

function startCountdown(time) {
    const countdownElement = document.getElementById("countdown");
    let remaining = time;

    countdownElement.innerHTML = `Countdown: ${remaining} sec`;

    const existingInterval = window.earthquakeInterval;
    if (existingInterval) {
        clearInterval(existingInterval);
    }

    window.earthquakeInterval = setInterval(() => {
        countdownElement.innerHTML = `Countdown: ${remaining} sec`;

        remaining--;

        if (remaining < 0) {
            clearInterval(window.earthquakeInterval);
            countdownElement.innerHTML = "⚠️ Strong shaking is happening now!";
        }
    }, 1000);
}

function showMapMarker() {
    const mapBox = document.getElementById("mapBox");
    mapBox.innerHTML = "Seismic Activity Zone";

    const marker = document.createElement("div");
    marker.classList.add("map-marker");

    const randomTop = Math.floor(Math.random() * 70) + 10;
    const randomLeft = Math.floor(Math.random() * 70) + 10;

    marker.style.top = randomTop + "%";
    marker.style.left = randomLeft + "%";

    mapBox.appendChild(marker);
}
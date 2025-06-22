function showGeolocateForm() {
    var form = document.getElementById('geolocate-form');
    form.style.display = 'block';
}

function geolocateIP() {
    var ipAddress = document.getElementById('ip-address').value;
    var resultContainer = document.getElementById('geolocation-result');

    // Clear previous results
    resultContainer.innerHTML = '';

    // Check if IP address is empty
    if (!ipAddress.trim()) {
        resultContainer.innerHTML = '<p>Please enter an IP address.</p>';
        return;
    }

    // Perform geolocation
    fetch('https://ipapi.co/' + ipAddress + '/json/')
        .then(response => response.json())
        .then(data => {
            // Display geolocation results
            if (data.error) {
                resultContainer.innerHTML = '<p>Failed to geolocate IP address.</p>';
            } else {
                var html = '<h3>Geolocation Results</h3>';
                html += '<p><strong>IP Address:</strong> ' + data.ip + '</p>';
                html += '<p><strong>Country:</strong> ' + data.country_name + '</p>';
                html += '<p><strong>City:</strong> ' + data.city + '</p>';
                html += '<p><strong>Region:</strong> ' + data.region + '</p>';

                // Check if IP address is private
                if (data.error || data.ip.startsWith('192.168.') || data.ip.startsWith('10.') || data.ip.startsWith('172.')) {
                    html += '<p>This is a private IP address.</p>';
                }

                resultContainer.innerHTML = html;
            }
        })
        .catch(error => {
            console.error('Error fetching geolocation:', error);
            resultContainer.innerHTML = '<p>Failed to fetch geolocation data.</p>';
        });
}

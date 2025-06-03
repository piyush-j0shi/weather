let userAgreedToDataUsage = false;

document.addEventListener('DOMContentLoaded', function() {
    // Show city input when "Yes" is selected
    document.querySelectorAll('input[name="checkWeather"]').forEach(radio => {
        radio.addEventListener('change', function() {
            const cityInput = document.getElementById('cityInput');
            if (this.value === 'yes') {
                cityInput.style.display = 'block';
                document.getElementById('currentCity').required = true;
            } else {
                cityInput.style.display = 'none';
                document.getElementById('currentCity').required = false;
                document.getElementById('currentCity').value = '';
            }
        });
    });

    // Handle form submission
    document.getElementById('weatherForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!userAgreedToDataUsage) {
            document.getElementById('dataModal').style.display = 'block';
            return;
        }
        
        submitWeatherForm();
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        const modal = document.getElementById('dataModal');
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});

function acceptDataUsage() {
    userAgreedToDataUsage = true;
    document.getElementById('dataModal').style.display = 'none';
    submitWeatherForm();
}

function declineDataUsage() {
    document.getElementById('dataModal').style.display = 'none';
    alert('To continue, please agree to the data usage terms.');
}

function clearResponseAfterDelay() {
    setTimeout(() => {
        // Clear response
        document.getElementById('responseText').textContent = '';
        document.getElementById('response').style.display = 'none';
        
        // Clear form fields
        document.getElementById('userName').value = '';
        document.getElementById('currentCity').value = '';
        
        // Reset radio buttons
        document.getElementById('no').checked = true;
        document.getElementById('yes').checked = false;
        
        // Hide city input
        document.getElementById('cityInput').style.display = 'none';
    }, 5000); // 5000 milliseconds = 5 seconds
}

async function submitWeatherForm() {
    const userName = document.getElementById('userName').value;
    const checkWeather = document.querySelector('input[name="checkWeather"]:checked').value;
    const currentCity = document.getElementById('currentCity').value;
    
    const submitBtn = document.getElementById('submitBtn');
    const progressContainer = document.getElementById('progressContainer');
    const response = document.getElementById('response');
    
    // Disable form and show progress
    submitBtn.disabled = true;
    progressContainer.style.display = 'block';
    response.style.display = 'none';
    
    // Simulate progress bar (10 seconds)
    if (checkWeather === 'yes') {
        await simulateProgress();
    }
    
    try {
        // Send data to backend
        const apiResponse = await fetch('/weather', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: userName,
                check_weather: checkWeather,
                city: currentCity
            })
        });
        
        const result = await apiResponse.json();
        
        // Show response
        document.getElementById('responseText').textContent = result.message;
        response.style.display = 'block';
        
        // Clear response and form fields after 5 seconds
        clearResponseAfterDelay();
        
        // Hide progress
        progressContainer.style.display = 'none';
        
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('responseText').textContent = 'An error occurred. Please try again.';
        response.style.display = 'block';
        progressContainer.style.display = 'none';
        
        // Clear error message and form fields after 5 seconds too
        clearResponseAfterDelay();
    }
    
    // Re-enable form
    submitBtn.disabled = false;
}

async function simulateProgress() {
    const progressFill = document.getElementById('progressFill');
    
    for (let i = 0; i <= 100; i++) {
        progressFill.style.width = i + '%';
        await new Promise(resolve => setTimeout(resolve, 100));
    }
}

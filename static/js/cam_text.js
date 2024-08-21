document.addEventListener('DOMContentLoaded', function() {
    const toggleSwitch = document.getElementById('toggleCheckbox');
    const accuracySwitch = document.getElementById('accuracyCheckbox');
    const cameraOutput = document.getElementById('video-feed');
    const outputBox = document.getElementById('output-box');

    function handleKeydown(event) {
        outputBox.value += event.key;
    }

    // Function to update the video feed URL based on the accuracy checkbox
    function updateVideoFeed() {
        const showAccuracy = accuracySwitch.checked ? "true" : "false";
        cameraOutput.src = `/video_key1?show_accuracy=${showAccuracy}`;
    }

    // Function to start the camera feed
    function startCamera() {
        updateVideoFeed(); // Update URL with current accuracy setting
        cameraOutput.style.display = 'block';
        document.addEventListener('keydown', handleKeydown);
    }

    // Function to stop the camera feed
    function stopCamera() {
        cameraOutput.src = "";  // Stop video stream
        cameraOutput.style.display = 'none';
        document.removeEventListener('keydown', handleKeydown);
        outputBox.value = ''; // Clear the text area
    }

    // Function to handle accuracy checkbox change
    function handleAccuracyChange() {
        // Turn off the camera, wait for 1 second, then turn it back on with the correct accuracy setting
        stopCamera();
        setTimeout(() => {
            updateVideoFeed();  // Update URL with new accuracy setting
            startCamera();  // Restart the camera feed
        }, 1000);
    }

    // Function to handle toggle switch change
    function handleToggleChange() {
        if (toggleSwitch.checked) {
            startCamera();
            accuracySwitch.disabled = false; // Enable accuracy checkbox
        } else {
            stopCamera();
            accuracySwitch.disabled = true; // Disable accuracy checkbox
        }
    }

    // Initialize camera based on the initial state of the toggle checkbox
    handleToggleChange();

    // Listen for changes to the camera toggle checkbox
    toggleSwitch.addEventListener('change', handleToggleChange);

    // Listen for changes to the accuracy checkbox
    accuracySwitch.addEventListener('change', handleAccuracyChange);
});

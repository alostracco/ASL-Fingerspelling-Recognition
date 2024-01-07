// main.js

let isVideoVisible = false;

function toggleVideo() {
    const videoElement = document.getElementById('video-stream');
    isVideoVisible = !isVideoVisible;

    if (isVideoVisible) {
        // Set the video feed URL when toggled on
        videoElement.src = videoFeedUrl;
    } else {
        // Set an empty or placeholder value when toggled off
        videoElement.src = "";
    }

    videoElement.style.display = isVideoVisible ? 'block' : 'none';
}

function toggleDarkMode() {
    console.log('object')
    document.body.classList.toggle('dark-mode'); // Toggle a class on the body
}
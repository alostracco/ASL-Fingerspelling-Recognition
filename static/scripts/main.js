// main.js

let isVideoVisible = true;

function toggleVideo() {
    const videoElement = document.getElementById('video-stream');
    isVideoVisible = !isVideoVisible;
    videoElement.style.display = isVideoVisible ? 'block' : 'none';
}

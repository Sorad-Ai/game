document.getElementById('fullscreenToggle').addEventListener('click', () => {
    const container = document.getElementById('container');
    const toggleIcon = document.getElementById('toggleIcon');

    if (!document.fullscreenElement) {
        container.requestFullscreen().then(() => {
            // Change to "exit fullscreen" icon
            toggleIcon.classList.remove('fa-expand');
            toggleIcon.classList.add('fa-compress');
        }).catch(err => {
            console.log(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
        });
    } else {
        document.exitFullscreen().then(() => {
            // Change back to "enter fullscreen" icon
            toggleIcon.classList.remove('fa-compress');
            toggleIcon.classList.add('fa-expand');
        }).catch(err => {
            console.log(`Error attempting to exit full-screen mode: ${err.message} (${err.name})`);
        });
    }
});

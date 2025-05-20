/**************************************************************************************************************
 * PLAYER INITIALIZATION AND PLAYBACK MANAGEMENT *
 **************************************************************************************************************/
let duration = 0;
let currentTime = 0;
let player;
let isPlaying = false;
let previousVolume = 100;

function onYouTubeIframeAPIReady() {
    const container = document.getElementById("youtube-audio");
    const playerContainer = document.createElement("div");
    playerContainer.setAttribute("id", "youtube-player");
    container.appendChild(playerContainer);

    container.onclick = function () {
        togglePlayPause();
    };

    player = new YT.Player("youtube-player", {
        height: "0",
        width: "0",
        videoId: container.dataset.video,
        playerVars: {
            autoplay: container.dataset.autoplay,
            loop: container.dataset.loop
        },
        events: {
            onReady: function (event) {
                duration = player.getDuration();
                updateUI();
                setInterval(updateTimeInfo, 1000);
                startTitleChecking();
                updateVolumeSlider();
                updateVolumeIcon();
            },
            onStateChange: function (event) {
                if (event.data === YT.PlayerState.ENDED || event.data === YT.PlayerState.PAUSED) {
                    isPlaying = false;
                } else if (event.data === YT.PlayerState.PLAYING) {
                    isPlaying = true;
                }
                updateUI();
            },
            onError: function (event) {
                showAlternativeLink(event.target.getVideoData().video_id);
            }
        }
    });

    // Hide player if the default video is set
    var defaultVideoId = "RMx7uHtZbuo";
    var containerVideoId = document.getElementById("youtube-audio").dataset.video;

    if (containerVideoId === defaultVideoId) {
        document.querySelector('.player').style.display = 'none';
    }
}

function initYouTube() {
    if (window.YT && YT.Player) {
        onYouTubeIframeAPIReady();
    } else {
        window.onYouTubeIframeAPIReady = onYouTubeIframeAPIReady;
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initYouTube);
} else {
    initYouTube();
}

function startTitleChecking() {
    const titleCheckInterval = setInterval(() => {
        const titleElement = document.getElementById('title');
        if (titleElement && titleElement.textContent.trim() !== "") {
            clearInterval(titleCheckInterval);
        } else if (!isPlaying) {
            showAlternativeLink(document.getElementById("youtube-audio").dataset.video);
        }
    }, 1000);
}

function togglePlayPause() {
    if (isPlaying) {
        player.pauseVideo();
    } else {
        player.playVideo();
    }
    isPlaying = !isPlaying;
    updateUI();
}

function updateTimeInfo() {
    currentTime = player.getCurrentTime();
    updateUI();
}

function formatTime(time) {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
}

function seekToTime(event) {
    const progressBar = document.getElementById('progressContainer');
    const clickPosition = event.clientX - progressBar.getBoundingClientRect().left;
    const percentage = clickPosition / progressBar.clientWidth;
    const seekTime = duration * percentage;
    player.seekTo(seekTime);
}

function updateTitle() {
    const currentTitleElement = document.getElementById('title');
    const videoData = player.getVideoData();
    currentTitleElement.textContent = videoData.title;
}

function updateUI() {
    const durationElement = document.getElementById('timeInfo');
    const progressBar = document.getElementById('progressBar');
    const progressThumb = document.getElementById('progressThumb');
    const progressPercentage = (currentTime / duration) * 100;

    progressBar.style.width = progressPercentage + '%';
    progressThumb.style.left = (progressPercentage - 1) + '%';

    const youtubeIcon = document.getElementById('youtube-icon');
    youtubeIcon.style.backgroundImage = `url(${isPlaying ? '/static/assets/img/pause.png' : '/static/assets/img/play.png'})`;

    durationElement.textContent = formatTime(currentTime) + ' / ' + formatTime(duration);

    updateTitle();
}

function showAlternativeLink(videoId) {
    const alternativeLinkDiv = document.getElementById('alternative-link');
    const playerContainer = document.getElementById('container');
    const loadingDiv = document.getElementById('title');

    if (loadingDiv.style.display !== 'none') {
        alternativeLinkDiv.style.display = '';
        alternativeLinkDiv.innerHTML = `<p>The audio/video available only on
        <a href="https://www.youtube.com/watch?v=${videoId}" target="_blank">
        <img id="youtube-logo" src="static/assets/img/YouTubeLogo.png" alt="YouTube Logo"> <br> Click to listen/watch.</a></p>`;

        playerContainer.style.display = 'none';
        loadingDiv.style.display = 'none';
    }
}

/*********************************************************************************************************************************************
 * PLAY TRACK BUTTONS MANAGEMENT *
 *********************************************************************************************************************************************/

function updateHTMLView(videoId) {
    const youtubePlayerDiv = document.getElementById('youtube-audio');
    youtubePlayerDiv.setAttribute('data-video', videoId);

    const titleElement = document.getElementById('title');
    const containerElement = document.getElementById('container');
    const alternativeLinkElement = document.getElementById('alternative-link');

    if (alternativeLinkElement.style.display === '' &&
        titleElement.style.display === 'none' &&
        containerElement.style.display === 'none') {
        titleElement.style.display = '';
        containerElement.style.display = '';
    } else {
        alternativeLinkElement.style.display = 'none';

        setTimeout(() => {
            if (titleElement.textContent.trim() !== '') {
                titleElement.style.display = '';
                containerElement.style.display = '';
            }
        }, 3000);
    }

    player.loadVideoById(videoId);
    isPlaying = true;
}

document.querySelectorAll('.play-button').forEach(button => {
    button.addEventListener('click', (event) => {
        const videoId = event.target.getAttribute('data-video-id');
        updateHTMLView(videoId);
        document.querySelector('.player').style.display = 'block';
    });
});

/*********************************************************************************************************************************************
 * VOLUME CONTROL *
 *********************************************************************************************************************************************/

function changeVolume(volume) {
    const volumeSlider = document.getElementById('volumeSlider');
    const volumeButton = document.getElementById('volumeButton');

    if (volume == 0) {
        player.mute();
        volumeButton.classList.add('muted');
    } else {
        player.unMute();
        player.setVolume(volume);
        volumeButton.classList.remove('muted');
    }

    volumeSlider.value = volume;
}

function toggleMute() {
    const volumeSlider = document.getElementById('volumeSlider');
    const volumeButton = document.getElementById('volumeButton');

    if (player.isMuted()) {
        player.unMute();
        player.setVolume(previousVolume);
        volumeSlider.value = previousVolume;
        volumeButton.classList.remove('muted');
    } else {
        previousVolume = volumeSlider.value;
        player.mute();
        volumeSlider.value = 0;
        volumeButton.classList.add('muted');
    }
}

function updateVolumeSlider() {
    const volumeSlider = document.getElementById('volumeSlider');
    if (player && volumeSlider) {
        const currentVolume = player.getVolume();
        volumeSlider.value = currentVolume;
    }
}

function updateVolumeIcon() {
    const volumeSlider = document.getElementById('volumeSlider');
    const volumeButton = document.getElementById('volumeButton');

    if (player.isMuted() || parseInt(volumeSlider.value) === 0) {
        volumeButton.classList.add('muted');
    } else {
        volumeButton.classList.remove('muted');
    }
}

document.getElementById('volumeSlider').addEventListener('input', function () {
    changeVolume(this.value);
    updateVolumeIcon();
});

document.getElementById('volume-icon').addEventListener('click', toggleMute);

/************************************************************************************************************************************************
 * PROGRESS BAR HANDLING *
 ************************************************************************************************************************************************/

function moveProgressThumb(event) {
    const progressBar = document.getElementById('progressContainer');
    const clickPosition = event.clientX - progressBar.getBoundingClientRect().left;
    const percentage = clickPosition / progressBar.clientWidth;
    const seekTime = duration * percentage;
    player.seekTo(seekTime);
}

document.getElementById('progressContainer').addEventListener('click', moveProgressThumb);

function smoothMoveProgressThumb() {
    const progressThumb = document.getElementById('progressThumb');
    progressThumb.style.transition = 'left 0.1s linear';
}

document.getElementById('progressThumb').addEventListener('transitionend', function () {
    this.style.transition = '';
    updateTimeInfo();
});

function updateProgressThumb() {
    const progressPercentage = (currentTime / duration) * 100;
    const progressThumb = document.getElementById('progressThumb');
    progressThumb.style.left = progressPercentage + '%';
}

setInterval(updateProgressThumb, 100);

function moveProgressThumbAndBar(event) {
    event.preventDefault();
    const progressBar = document.getElementById('progressContainer');
    const clickPosition = event.clientX - progressBar.getBoundingClientRect().left;
    let percentage = clickPosition / progressBar.clientWidth;
    percentage = Math.max(0, Math.min(1, percentage));

    const seekTime = duration * percentage;
    player.seekTo(seekTime);

    document.getElementById('progressThumb').style.left = percentage * 100 + '%';
    document.getElementById('progressBar').style.width = percentage * 100 + '%';
}

document.getElementById('progressContainer').addEventListener('mousedown', function (event) {
    moveProgressThumbAndBar(event);
    document.addEventListener('mousemove', moveProgressThumbAndBar);
    function handleMouseUp() {
        document.removeEventListener('mousemove', moveProgressThumbAndBar);
        document.removeEventListener('mouseup', handleMouseUp);
    }
    document.addEventListener('mouseup', handleMouseUp);
});

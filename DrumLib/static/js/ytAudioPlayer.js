/**************************************************************************************************************
 * PLAYER INITIALIZATION AND PLAYBACK MANAGEMENT *
 **************************************************************************************************************/

var duration;
var currentTime;
var player;
var isPlaying = false;
var previousVolume;


// Function called when the YouTube Iframe API is ready
function onYouTubeIframeAPIReady() {
    var container = document.getElementById("youtube-audio");
    var playerContainer = document.createElement("div");
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
                updateVolumeIcon(); // Call the function when the player is ready
            },
            onStateChange: function (event) {
                if (event.data === YT.PlayerState.ENDED) {
                    isPlaying = false;
                } else if (event.data === YT.PlayerState.PLAYING) {
                    isPlaying = true;
                } else if (event.data === YT.PlayerState.PAUSED) {
                    isPlaying = false;
                }
                updateUI();
            },
            onError: function (event) {
                showAlternativeLink(event.target.getVideoData().video_id);
            },
            onVolumeChange: updateVolumeIcon // Call the function when volume changes
        }
    });
}



// Function to start checking for title availability
function startTitleChecking() {
    var titleCheckInterval = setInterval(function() {
        var titleElement = document.getElementById('title');
        console.log("Title Element:", titleElement);
        console.log("Title Content:", titleElement.textContent.trim());
        console.log("Condition:", titleElement && titleElement.textContent.trim() !== "");
        if (titleElement && titleElement.textContent.trim() !== "") {
            clearInterval(titleCheckInterval);
        } else {

            if (!isPlaying) {
                console.log("Show Alternative Link!");
                showAlternativeLink(document.getElementById("youtube-audio").dataset.video);
            }
        }
    }, 1000);
}



// Function to toggle play/pause
function togglePlayPause() {
    if (isPlaying) {
        player.pauseVideo();
    } else {
        player.playVideo();
    }
    isPlaying = !isPlaying;
    updateUI();
}



// Function to update time information
function updateTimeInfo() {
    currentTime = player.getCurrentTime();
    updateUI();
}



// Function to format time
function formatTime(time) {
    var minutes = Math.floor(time / 60);
    var seconds = Math.floor(time % 60);
    return minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
}


// Function to seek to a specific time
function seekToTime(event) {
    var progressBar = document.getElementById('progressContainer');
    var clickPosition = event.clientX - progressBar.getBoundingClientRect().left;
    var percentage = clickPosition / progressBar.clientWidth;
    var seekTime = duration * percentage;
    player.seekTo(seekTime);
}


// Function to update the video title
function updateTitle() {
    var currentTitleElement = document.getElementById('title');
    var videoData = player.getVideoData();
    var title = videoData.title;

    currentTitleElement.textContent = title;
}

// Function to update the UI
function updateUI() {
    var durationElement = document.getElementById('timeInfo');
    var progressBar = document.getElementById('progressBar');
    var progressThumb = document.getElementById('progressThumb');
    var progressContainer = document.getElementById('progressContainer');
    var progressPercentage = (currentTime / duration) * 100;
    progressBar.style.width = progressPercentage + '%';
    progressThumb.style.left = (progressPercentage - 1) + '%';

    var youtubeIcon = document.getElementById('youtube-icon');
    youtubeIcon.style.backgroundImage = 'url(' + (isPlaying ? '/static/assets/img/pause.png' : '/static/assets/img/play.png') + ')';

    var formattedTime = formatTime(currentTime) + ' / ' + formatTime(duration);
    durationElement.textContent = formattedTime;

    updateTitle();
}


// Function to display an alternative link
function showAlternativeLink(videoId) {
    var alternativeLinkDiv = document.getElementById('alternative-link');
    var playerContainer = document.getElementById('container');
    var loadingDiv = document.getElementById('title');

    if (loadingDiv.style.display !== 'none') {
        alternativeLinkDiv.style.display = '';
        alternativeLinkDiv.innerHTML = '<p>The audio/video available only on <a href="https://www.youtube.com/watch?v=' + videoId + '" target="_blank"><img id="youtube-logo" src="static/assets/img/YouTubeLogo.png" alt="YouTube Logo"> <br> Click to listen/watch.</a></p>';

        playerContainer.style.display = 'none';
        loadingDiv.style.display = 'none';
    }
}


/*********************************************************************************************************************************************
 * PLAY TRACK BUTTONS MANAGEMENT *
 *********************************************************************************************************************************************/
var buttons = document.querySelectorAll('.play-button');
console.log(buttons);

function updateHTMLView(videoId) {
    var youtubePlayerDiv = document.getElementById('youtube-audio');
    youtubePlayerDiv.setAttribute('data-video', videoId);

    var youtubePlayerIFrame = document.getElementById('youtube-player');
    var youtubePlayerSrc = "https://www.youtube.com/embed/" + videoId + "?autoplay=1&loop=1&enablejsapi=1";
    youtubePlayerIFrame.setAttribute('src', youtubePlayerSrc);
    var titleElement = document.getElementById('title');
    var containerElement = document.getElementById('container');
    var alternativeLinkElement = document.getElementById('alternative-link');

    if (alternativeLinkElement.style.display === '' &&
        titleElement.style.display === 'none' &&
        containerElement.style.display === 'none') {
        titleElement.style.display = '';
        containerElement.style.display = '';
    } else {
        alternativeLinkElement.style.display = 'none';

        setTimeout(function() {
            if (titleElement.textContent.trim() !== '') {
                titleElement.style.display = '';
                containerElement.style.display = '';
            }
        }, 3000);
    }

    isPlaying = true;
}


document.addEventListener('click', function(event) {
    if (event.target.classList.contains('play-button')) {
        var button = event.target;
        var videoId = button.getAttribute('data-video-id');

        updateHTMLView(videoId);
        console.log('data-video updated to:', videoId);
        console.log('Clicked button with videoId:', videoId);
    }
});

document.querySelector('.player').style.display = 'none';

document.addEventListener('click', function(event) {
    if (event.target.classList.contains('play-button')) {
        var button = event.target;
        var videoId = button.getAttribute('data-video-id');

        updateHTMLView(videoId);
        console.log('data-video updated to:', videoId);

        document.querySelector('.player').style.display = 'block';

        console.log('Clicked button with videoId:', videoId);
    }
});


/*********************************************************************************************************************************************
 * VOLUME CONTROL AND VOLUME ICON *
 *********************************************************************************************************************************************/


// Function to update volume button based on volume slider value
function updateVolumeButton() {
  var volumeSlider = document.getElementById('volumeSlider');
  var volumeButton = document.getElementById('volumeButton');

  if (player.isMuted() || player.getVolume() === 0) {
      volumeButton.classList.add('muted');
  } else {
      volumeButton.classList.remove('muted');
  }
}

// Call the function to update volume button after each volume change
document.getElementById('volumeSlider').addEventListener('input', updateVolumeButton);


// Function to change volume
function changeVolume(volume) {
  var volumeSlider = document.getElementById('volumeSlider');
  var volumeButton = document.getElementById('volumeButton');

  if (volume === 0) {
      volumeButton.classList.add('muted');
      volumeSlider.value = 0;
      player.mute();
  } else {
      volumeButton.classList.remove('muted');
      volumeSlider.value = volume;
      player.unMute();
  }

  player.setVolume(volume);
}


// Function to update volume slider value based on current player volume
function updateVolumeSlider() {
  var volumeSlider = document.getElementById('volumeSlider');
  if (player && volumeSlider) {
      var currentVolume = player.getVolume();
      volumeSlider.value = currentVolume;
  }
}

// Call the function to update volume slider after the player is ready
player.addEventListener('onReady', updateVolumeSlider);

var previousVolume = 100;



function toggleMute() {
  var volumeSlider = document.getElementById('volumeSlider');
  var volumeButton = document.getElementById('volumeButton');

  if (player.isMuted()) {

      player.unMute();
      volumeButton.classList.remove('muted');
      volumeSlider.value = previousVolume;
      player.setVolume(previousVolume);
  } else {
      previousVolume = volumeSlider.value;
      player.mute();
      volumeButton.classList.add('muted');
      volumeSlider.value = 0;
  }
}

// Add event handling for the volume icon click
document.getElementById('volume-icon').addEventListener('click', function() {
  toggleMute();
});


function updateVolumeIcon() {
  var volumeButton = document.getElementById('volumeButton');
  if (volumeButton) {
      var volumeSlider = document.getElementById('volumeSlider');
      var volumeValue = parseInt(volumeSlider.value);

      if (volumeValue === 0) {
          volumeButton.classList.add('muted');
      } else {
          volumeButton.classList.remove('muted');
      }
  }
}


document.getElementById('volumeSlider').addEventListener('input', updateVolumeIcon);


/************************************************************************************************************************************************
 * PROGRESS BAR HANDLING *
 ************************************************************************************************************************************************/

// Function to move the progress thumb when clicked
function moveProgressThumb(event) {
    var progressBar = document.getElementById('progressContainer');

    var clickPosition = event.clientX - progressBar.getBoundingClientRect().left;

    var percentage = clickPosition / progressBar.clientWidth;

    var seekTime = duration * percentage;

    player.seekTo(seekTime);

    var progressThumb = document.getElementById('progressThumb');
    progressThumb.style.left = percentage * 100 + '%';
}

document.getElementById('progressContainer').addEventListener('click', moveProgressThumb);


// Function for smooth transition of the progress thumb
function smoothMoveProgressThumb() {
    var progressThumb = document.getElementById('progressThumb');
    progressThumb.style.transition = 'left 0.1s linear';
}

document.getElementById('progressThumb').addEventListener('transitionend', function() {
    this.style.transition = '';
});



// Function to update the time on seeking
function updateTimeOnSeek() {
    currentTime = player.getCurrentTime();
    updateUI();
}

document.getElementById('progressThumb').addEventListener('transitionend', updateTimeOnSeek);



// Function to continuously update the progress thumb position based on the current time
function updateProgressThumb() {
    var progressPercentage = (currentTime / duration) * 100;

    var progressThumb = document.getElementById('progressThumb');
    progressThumb.style.left = progressPercentage + '%';
}

setInterval(updateProgressThumb, 100);



// Function to move the progress thumb and progress bar together when clicked and dragged
function moveProgressThumbAndBar(event) {
    event.preventDefault();

    var progressBar = document.getElementById('progressContainer');
    var clickPosition = event.clientX - progressBar.getBoundingClientRect().left;
    var percentage = clickPosition / progressBar.clientWidth;

    percentage = Math.max(0, Math.min(1, percentage));

    var seekTime = duration * percentage;

    player.seekTo(seekTime);

    var progressThumb = document.getElementById('progressThumb');
    progressThumb.style.left = percentage * 100 + '%';

    var progressBar = document.getElementById('progressBar');
    progressBar.style.width = percentage * 100 + '%';
}

document.getElementById('progressContainer').addEventListener('mousedown', function(event) {
    moveProgressThumbAndBar(event);
    document.addEventListener('mousemove', moveProgressThumbAndBar);

    // Function to handle mouseup event
    function handleMouseUp() {
        document.removeEventListener('mousemove', moveProgressThumbAndBar);
        document.removeEventListener('mouseup', handleMouseUp);
    }

    document.addEventListener('mouseup', handleMouseUp);
});
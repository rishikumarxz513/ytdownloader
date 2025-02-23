function fetchThumbnail() {
    const videoUrl = document.getElementById('videoUrl').value;
    if (videoUrl) {
        fetch('/thumbnail', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: videoUrl })
        })
        .then(response => response.json())
        .then(data => {
            if (data.thumbnail) {
                const thumbnailContainer = document.getElementById('thumbnailContainer');
                thumbnailContainer.innerHTML = '';
                const img = document.createElement('img');
                img.src = data.thumbnail;
                thumbnailContainer.appendChild(img);
            }
        })
        .catch(error => {
            console.error('Error fetching thumbnail:', error);
        });
    }
}

document.getElementById('downloadChoice').addEventListener('change', function() {
    const choice = this.value;
    const videoUrl = document.getElementById('videoUrl').value;
    if (choice === 'video' && videoUrl) {
        fetch('/video-options', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: videoUrl })
        })
        .then(response => response.json())
        .then(data => {
            const videoOptionsContainer = document.getElementById('videoOptionsContainer');
            videoOptionsContainer.innerHTML = '<select id="videoQuality">' +
                data.options.map(option => `<option value="${option}">${option}</option>`).join('') +
                '</select>';
        });
    }
});

document.getElementById('downloadButton').addEventListener('click', function() {
    const videoUrl = document.getElementById('videoUrl').value;
    const choice = document.getElementById('downloadChoice').value;
    const quality = choice === 'video' ? document.getElementById('videoQuality').value : null;

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: videoUrl, choice: choice, quality: quality })
    })
    .then(response => response.json())
    .then(data => {
        if (data.thumbnail) {
            const img = document.createElement('img');
            img.src = data.thumbnail;
            document.getElementById('thumbnailContainer').appendChild(img);
        }

        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        progressBar.style.width = '0%';
        progressText.innerText = '';

        const intervalId = setInterval(() => {
            fetch('/progress')
                .then(response => response.json())
                .then(progressData => {
                    progressBar.style.width = `${progressData.progress}%`;
                    progressText.innerText = `Download progress: ${progressData.progress}%`;
                    if (progressData.progress >= 100) {
                        clearInterval(intervalId);
                    }
                });
        }, 1000); // Poll every second

        if (data.message) {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to download. Please try again.');
    });
});

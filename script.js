const API_KEY = 'AIzaSyAIuRRH4V1aofNSGCV1DLTqAkQ5Jtrm-tk'; // Замените на свой ключ API
const SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search';

document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('query').value;
    searchYouTube(query);
});

function searchYouTube(query) {
    fetch(`${SEARCH_URL}?part=snippet&q=${encodeURIComponent(query)}&key=${API_KEY}&type=video&maxResults=10`)
        .then(response => response.json())
        .then(data => {
            displayResults(data.items);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function displayResults(videos) {
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = '';

    videos.forEach(video => {
        const videoId = video.id.videoId;
        const title = video.snippet.title;
        const thumbnail = video.snippet.thumbnails.high.url;
        const publishedAt = video.snippet.publishedAt.substring(0, 10);

        const videoElement = document.createElement('div');
        videoElement.className = 'video-container';
        videoElement.innerHTML = `
            <a href="video.html?video_id=${videoId}" class="video-link">
                <img src="${thumbnail}" alt="${title}">
                <h2>${title}</h2>
                <p class="published-at">Published on: ${publishedAt}</p>
            </a>
        `;
        resultsContainer.appendChild(videoElement);
    });
}

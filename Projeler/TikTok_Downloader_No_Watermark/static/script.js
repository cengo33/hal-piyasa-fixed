document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const navItems = document.querySelectorAll('.nav-item');
    const views = document.querySelectorAll('.view');
    const fetchBtn = document.getElementById('fetchBtn');
    const tiktokUrlInput = document.getElementById('tiktokUrl');
    const resultContainer = document.getElementById('resultContainer');
    const errorMsg = document.getElementById('errorMsg');
    const tiktokFeed = document.getElementById('tiktokFeed');
    const pasteBtn = document.getElementById('pasteBtn');

    // Video Result Elements
    const videoCover = document.getElementById('videoCover');
    const videoTitle = document.getElementById('videoTitle');
    const videoAuthor = document.getElementById('videoAuthor');
    const downloadBtn = document.getElementById('downloadBtn');
    const musicBtn = document.getElementById('musicBtn');

    // --- NAVIGATION ---
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetView = item.getAttribute('data-view');
            
            // Update Sidebar
            navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');

            // Update View
            views.forEach(v => v.classList.remove('active'));
            document.getElementById(targetView + 'View').classList.add('active');

            // Load feed if switching to explore
            if (targetView === 'explore' && tiktokFeed.children.length <= 1) {
                loadTrendingFeed();
            }
        });
    });

    // --- DOWNLOADER LOGIC ---
    fetchBtn.addEventListener('click', async () => {
        const url = tiktokUrlInput.value.trim();
        if (!url) return showError('Please paste a TikTok URL');

        setLoading(true);
        hideError();
        resultContainer.classList.add('hidden');

        try {
            const response = await fetch('/api/fetch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url }),
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to fetch info');

            displayResult(data);
        } catch (err) {
            showError(err.message);
        } finally {
            setLoading(false);
        }
    });

    function displayResult(data) {
        videoCover.src = data.cover;
        videoTitle.textContent = data.title || 'No Title';
        videoAuthor.textContent = `@${data.author}`;
        
        const safeTitle = (data.title || 'tiktok_video').substring(0, 30).replace(/[^a-z0-9]/gi, '_').toLowerCase();
        const downloadUrl = `/api/download?url=${encodeURIComponent(data.no_wm_url)}&filename=${safeTitle}_no_wm.mp4`;
        
        downloadBtn.onclick = (e) => {
            window.location.href = downloadUrl;
            e.preventDefault();
        };
        musicBtn.href = data.music_url;

        resultContainer.classList.remove('hidden');
        
        // Switch to downloader view if not already there
        switchToView('download');
    }

    // --- EXPLORE / FEED LOGIC ---
    async function loadTrendingFeed() {
        try {
            const response = await fetch('/api/feed');
            const data = await response.json();

            if (data.code !== 0) throw new Error('Could not load feed');

            tiktokFeed.innerHTML = ''; // Clear loader
            data.data.forEach(video => {
                const item = document.createElement('div');
                item.className = 'feed-item';
                // TikWM feed uses video_id
                const vId = video.video_id || video.id;
                const authorId = video.author.unique_id;
                
                item.innerHTML = `
                    <img src="${video.cover}" alt="cover">
                    <div class="btn-quick-dl"><i class="fas fa-arrow-down"></i></div>
                    <div class="item-overlay">
                        <p class="item-author">@${video.author.nickname}</p>
                        <p class="item-title">${video.title || ''}</p>
                    </div>
                `;
                
                item.addEventListener('click', () => {
                    const originUrl = `https://www.tiktok.com/@${authorId}/video/${vId}`;
                    tiktokUrlInput.value = originUrl;
                    fetchBtn.click();
                });

                tiktokFeed.appendChild(item);
            });
        } catch (err) {
            tiktokFeed.innerHTML = `<div class="error-msg">Failed to load trending feed.</div>`;
        }
    }

    // --- HELPERS ---
    function switchToView(viewId) {
        const item = document.querySelector(`.nav-item[data-view="${viewId}"]`);
        if (item) item.click();
    }

    function setLoading(isLoading) {
        fetchBtn.classList.toggle('loading', isLoading);
        fetchBtn.disabled = isLoading;
    }

    function showError(msg) {
        errorMsg.textContent = msg;
        errorMsg.classList.remove('hidden');
    }

    function hideError() {
        errorMsg.classList.add('hidden');
    }

    pasteBtn.addEventListener('click', async () => {
        try {
            const text = await navigator.clipboard.readText();
            tiktokUrlInput.value = text;
            if (text.includes('tiktok.com')) {
                fetchBtn.click();
            }
        } catch (err) {
            alert('Please allow clipboard access or paste manually.');
        }
    });

    tiktokUrlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') fetchBtn.click();
    });
});

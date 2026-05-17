document.addEventListener('DOMContentLoaded', () => {
    // Theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    
    // Check local storage for theme
    if (localStorage.getItem('theme') === 'dark') {
        html.setAttribute('data-theme', 'dark');
        if (themeToggle) themeToggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            if (html.getAttribute('data-theme') === 'dark') {
                html.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
                themeToggle.innerHTML = '<i class="bi bi-moon-fill"></i>';
            } else {
                html.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                themeToggle.innerHTML = '<i class="bi bi-sun-fill"></i>';
            }
        });
    }

    // Like functionality
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const postId = btn.dataset.post;
            try {
                const response = await fetch(`/posts/like/${postId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                const data = await response.json();
                const icon = btn.querySelector('i');
                const countSpan = btn.querySelector('.like-count');
                
                if (data.status === 'liked') {
                    icon.classList.remove('bi-heart');
                    icon.classList.add('bi-heart-fill');
                    btn.classList.add('liked');
                } else {
                    icon.classList.remove('bi-heart-fill');
                    icon.classList.add('bi-heart');
                    btn.classList.remove('liked');
                }
                countSpan.textContent = data.likes_count;
            } catch (error) {
                console.error('Error liking post:', error);
            }
        });
    });

    // Save functionality
    document.querySelectorAll('.save-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const postId = btn.dataset.post;
            try {
                const response = await fetch(`/posts/save/${postId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                const data = await response.json();
                const icon = btn.querySelector('i');
                
                if (data.status === 'saved') {
                    icon.classList.remove('bi-bookmark');
                    icon.classList.add('bi-bookmark-fill');
                    btn.classList.add('saved');
                } else {
                    icon.classList.remove('bi-bookmark-fill');
                    icon.classList.add('bi-bookmark');
                    btn.classList.remove('saved');
                }
            } catch (error) {
                console.error('Error saving post:', error);
            }
        });
    });
});

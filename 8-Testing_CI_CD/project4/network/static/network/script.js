document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-button').forEach(button => {
        button.onclick = () => {
            const postId = button.dataset.postId;
            fetch(`/like/${postId}`, {
                method: 'PUT'
            })
            .then(response => response.json())
            .then(result => {
                if (result.liked) {
                    button.innerHTML = 'Unlike';
                } else {
                    button.innerHTML = 'Like';
                }
                button.nextElementSibling.innerHTML = `Likes: ${result.likes_count}`;
            });
        };
    });

    document.querySelectorAll('.edit-button').forEach(button => {
        button.onclick = () => {
            const postId = button.dataset.postId;
            const postContent = button.previousElementSibling.previousElementSibling;
            const textarea = document.createElement('textarea');
            textarea.value = postContent.innerHTML;
            postContent.replaceWith(textarea);
            button.innerHTML = 'Save';
            button.onclick = () => {
                fetch(`/edit/${postId}`, {
                    method: 'POST',
                    body: JSON.stringify({
                        content: textarea.value
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(result => {
                    if (result.message) {
                        textarea.replaceWith(postContent);
                        postContent.innerHTML = textarea.value;
                        button.innerHTML = 'Edit';
                    }
                });
            };
        };
    });

    const followButton = document.getElementById('follow-button');
    if (followButton) {
        followButton.onclick = () => {
            const username = followButton.dataset.username;
            fetch(`/follow/${username}`, {
                method: 'PUT'
            })
            .then(() => {
                if (followButton.innerHTML === 'Follow') {
                    followButton.innerHTML = 'Unfollow';
                } else {
                    followButton.innerHTML = 'Follow';
                }
            });
        };
    }
});
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".like-button").forEach(button => {
        button.onclick = function () {
            const postId = this.dataset.postId;
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/like/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                // Actualizar el conteo de likes en la interfaz de usuario
                const likeCountElement = button.parentElement.querySelector('.like-count');
                likeCountElement.innerHTML = `❤️ ${data.likes_count}`;

                // Actualizar el texto del botón
                if (data.liked) {
                    button.innerHTML = 'Unlike';
                } else {
                    button.innerHTML = 'Like';
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        };
    });

    const followButton = document.getElementById('follow-button');
    if (followButton) {
        followButton.onclick = () => {
            const username = followButton.dataset.username;
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/follow/${username}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                // Actualizar el conteo de seguidores en la interfaz de usuario
                document.getElementById('followers-count').innerHTML = data.followers;

                // Actualizar el texto del botón
                if (data.is_following) {
                    followButton.innerHTML = 'Unfollow';
                } else {
                    followButton.innerHTML = 'Follow';
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        };
    }
});

document.querySelectorAll('.edit-button').forEach(button => {
    button.onclick = () => {
        const postId = button.dataset.postId;
        const postContent = button.previousElementSibling.previousElementSibling;
        const textarea = document.createElement('textarea');
        textarea.value = postContent.innerHTML;
    };
});


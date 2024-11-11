document.addEventListener("DOMContentLoaded", function () {
  function setupLikeButtons() {
    document.querySelectorAll(".like-button").forEach((button) => {
      button.onclick = function () {
        const postId = this.dataset.postId;
        const csrfTokenElement = document.querySelector(
          "[name=csrfmiddlewaretoken]"
        );
        if (!csrfTokenElement) {
          console.error("CSRF token not found");
          return;
        }
        const csrftoken = csrfTokenElement.value;

        fetch(`/like/${postId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({}),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.liked) {
              button.innerHTML = "Unlike";
            } else {
              button.innerHTML = "Like";
            }
            const likeCountElement =
              button.parentElement.querySelector(".like-count span");
            likeCountElement.innerHTML = data.likes_count;
          })
          .catch((error) => {
            console.error(
              "There was a problem with the fetch operation:",
              error
            );
          });
      };
    });
  }

  setupLikeButtons();

  const followButton = document.getElementById("follow-button");
  if (followButton) {
    followButton.onclick = () => {
      const username = followButton.dataset.username;
      const csrftoken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;

      fetch(`/follow/${username}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({}),
      })
        .then((response) => response.json())
        .then((data) => {
          document.getElementById("followers-count").innerHTML = data.followers;
          if (data.is_following) {
            followButton.innerHTML = "Unfollow";
          } else {
            followButton.innerHTML = "Follow";
          }
        })
        .catch((error) => {
          console.error("There was a problem with the fetch operation:", error);
        });
    };
  }

  document.querySelectorAll(".edit-button").forEach((button) => {
    button.onclick = () => {
      const postId = button.dataset.postId;
      const postContent = button.previousElementSibling.previousElementSibling;
      const textarea = document.createElement("textarea");
      textarea.value = postContent.innerHTML;
      postContent.replaceWith(textarea);
      button.innerHTML = "Save";
      button.onclick = () => {
        fetch(`/edit_post/${postId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
              .value,
          },
          body: JSON.stringify({
            content: textarea.value,
          }),
        })
          .then((response) => response.json())
          .then((result) => {
            if (result.message) {
              textarea.replaceWith(postContent);
              postContent.innerHTML = textarea.value;
              button.innerHTML = "Edit";
            } else {
              console.error(result.error);
            }
          });
      };
    };
  });
});

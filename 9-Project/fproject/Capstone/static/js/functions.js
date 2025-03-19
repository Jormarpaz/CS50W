//
// Funciones para arrastrar y soltar archivos
//
function allowDrop(event) {
  event.preventDefault();
}

function drag(event) {
  const fileElement = event.target.closest(".file");
  if (!fileElement) return;

  const fileId = fileElement.dataset.fileId;
  event.dataTransfer.setData("text", fileId);
}

function drop(event) {
  event.preventDefault();
  const fileId = event.dataTransfer.getData("text");
  const targetFolderElement = event.target.closest(".folder");
  const targetFolderId = targetFolderElement
    ? targetFolderElement.dataset.folderId
    : null;

  fetch(MOVE_FILE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": CSRF_TOKEN,
    },
    body: JSON.stringify({ file_id: fileId, folder_id: targetFolderId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        location.reload(); // Recargar la página para reflejar los cambios
      } else {
        console.error("Error al mover el archivo:", data.error);
      }
    })
    .catch((error) => {
      console.error("Error en la solicitud de mover archivo:", error);
    });
}
//
// Funciones para eliminar archivos y carpetas
//
function toggleFileCheckboxes() {
  const checkboxes = document.querySelectorAll(
    ".delete-checkbox[data-type='file']"
  );
  const confirmButton = document.getElementById("confirm-delete");
  const cancelButton = document.getElementById("cancel-delete");
  const deleteButton = document.querySelector(
    "button[onclick='toggleFileCheckboxes()']"
  );
  const folderDeleteButton = document.querySelector(
    "button[onclick='toggleFolderCheckboxes()']"
  );

  // Verificar si las variables están definidas antes de usarlas
  const uploadButton =
    typeof FILE_UPLOAD_URL !== "undefined"
      ? document.querySelector(`a[href='${FILE_UPLOAD_URL}']`)
      : null;
  const createFolderButton =
    typeof CREATE_FOLDER_URL !== "undefined"
      ? document.querySelector(`a[href='${CREATE_FOLDER_URL}']`)
      : null;
  const createSubfolderButton =
    typeof CREATE_SUBFOLDER_URL !== "undefined"
      ? document.querySelector(`a[href='${CREATE_SUBFOLDER_URL}']`)
      : null;
  const uploadsubfolderButton =
    typeof SUBFILE_UPLOAD_URL !== "undefined"
      ? document.querySelector(`a[href='${SUBFILE_UPLOAD_URL}']`)
      : null;

  checkboxes.forEach((checkbox) => {
    if (checkbox)
      checkbox.style.display =
        checkbox.style.display === "none" ? "inline-block" : "none";
  });

  if (confirmButton) confirmButton.style.display = "inline-block";
  if (cancelButton) cancelButton.style.display = "inline-block";
  if (deleteButton) deleteButton.style.display = "none";
  if (folderDeleteButton) folderDeleteButton.style.display = "none";
  if (uploadButton) uploadButton.style.display = "none";
  if (createFolderButton) createFolderButton.style.display = "none";
  if (createSubfolderButton) createSubfolderButton.style.display = "none";
  if (uploadsubfolderButton) uploadsubfolderButton.style.display = "none";
}

function toggleFolderCheckboxes() {
  const checkboxes = document.querySelectorAll(
    ".delete-checkbox[data-type='folder']"
  );
  const confirmButton = document.getElementById("confirm-delete");
  const cancelButton = document.getElementById("cancel-delete");
  const deleteButton = document.querySelector(
    "button[onclick='toggleFileCheckboxes()']"
  );
  const folderDeleteButton = document.querySelector(
    "button[onclick='toggleFolderCheckboxes()']"
  );

  // Verificar si las variables están definidas antes de usarlas
  const uploadButton =
    typeof FILE_UPLOAD_URL !== "undefined"
      ? document.querySelector(`a[href='${FILE_UPLOAD_URL}']`)
      : null;
  const createFolderButton =
    typeof CREATE_FOLDER_URL !== "undefined"
      ? document.querySelector(`a[href='${CREATE_FOLDER_URL}']`)
      : null;
  const createSubfolderButton =
    typeof CREATE_SUBFOLDER_URL !== "undefined"
      ? document.querySelector(`a[href='${CREATE_SUBFOLDER_URL}']`)
      : null;
  const uploadsubfolderButton =
    typeof SUBFILE_UPLOAD_URL !== "undefined"
      ? document.querySelector(`a[href='${SUBFILE_UPLOAD_URL}']`)
      : null;

  checkboxes.forEach((checkbox) => {
    if (checkbox)
      checkbox.style.display =
        checkbox.style.display === "none" ? "inline-block" : "none";
  });

  // Ocultar archivos dentro de las carpetas
  const folderContents = document.querySelectorAll(".folder ul");
  folderContents.forEach((content) => {
    if (content)
      content.style.display =
        checkboxes[0] && checkboxes[0].style.display === "inline-block"
          ? "none"
          : "block";
  });

  // Ocultar mensajes de "Vacía" dentro de las carpetas
  const folderEmptyMessages = document.querySelectorAll(
    ".folder .empty-message"
  );
  folderEmptyMessages.forEach((message) => {
    if (message)
      message.style.display =
        checkboxes[0] && checkboxes[0].style.display === "inline-block"
          ? "none"
          : "block";
  });

  if (confirmButton) confirmButton.style.display = "inline-block";
  if (cancelButton) cancelButton.style.display = "inline-block";
  if (deleteButton) deleteButton.style.display = "none";
  if (folderDeleteButton) folderDeleteButton.style.display = "none";
  if (uploadButton) uploadButton.style.display = "none";
  if (createFolderButton) createFolderButton.style.display = "none";
  if (createSubfolderButton) createSubfolderButton.style.display = "none";
  if (uploadsubfolderButton) uploadsubfolderButton.style.display = "none";
}

function confirmDelete() {
  const checkboxes = document.querySelectorAll(".delete-checkbox:checked");
  const ids = Array.from(checkboxes).map((checkbox) => checkbox.value);
  const types = Array.from(checkboxes).map((checkbox) => checkbox.dataset.type);

  const deletePromises = ids.map((id, index) => {
    const type = types[index];
    const url = type === "file" ? DELETE_FILE_URL : DELETE_FOLDER_URL;

    return fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": CSRF_TOKEN,
      },
      body: JSON.stringify({ [`${type}_id`]: id }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          const checkbox = document.querySelector(
            `.delete-checkbox[value="${id}"]`
          );
          if (checkbox) {
            //checkbox.parentElement.remove();
            checkbox.closest("li").remove();
          }
        } else {
          console.error(`Error al eliminar ${type}:`, data.error);
        }
      })
      .catch((error) => {
        console.error(
          `Error en la solicitud de eliminación de ${type}:`,
          error
        );
      });
  });

  Promise.all(deletePromises).then(() => {
    location.reload();
  });
}

function cancelDelete() {
  location.reload();
}

// Llamar a checkIfEmpty() después de crear una subcarpeta
document.addEventListener("DOMContentLoaded", function () {
  const createFolderForm = document.querySelector(
    "form[action='${CREATE_FOLDER_URL}']"
  );
  if (createFolderForm) {
    createFolderForm.addEventListener("submit", function (event) {
      event.preventDefault();
      fetch(createFolderForm.action, {
        method: "POST",
        body: new FormData(createFolderForm),
        headers: {
          "X-CSRFToken": CSRF_TOKEN,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            location.reload(); // Recargar la página para reflejar los cambios
          } else {
            console.error("Error al crear la carpeta:", data.error);
          }
        })
        .catch((error) => {
          console.error("Error en la solicitud de creación de carpeta:", error);
        });
    });
  }
});

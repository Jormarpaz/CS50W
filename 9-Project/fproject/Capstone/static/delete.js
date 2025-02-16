function deleteFile(fileId) {
    if (!confirm("¿Seguro que quieres eliminar este archivo?")) return;

    fetch("/delete-file/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ file_id: fileId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert("Error al eliminar archivo: " + data.error);
        }
    });
}

function deleteFolder(folderId) {
    if (!confirm("¿Seguro que quieres eliminar esta carpeta y su contenido?")) return;

    fetch("/delete-folder/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ folder_id: folderId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert("Error al eliminar carpeta: " + data.error);
        }
    });
}

// Función para obtener el token CSRF
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

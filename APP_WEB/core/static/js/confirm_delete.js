$(document).ready(function() {
    $('.delete-user').click(function(event) {
        event.preventDefault();
        var userId = $(this).data('user-id');
        
        var confirmation = confirm("¿Estás seguro de que quieres eliminar este usuario?");
        if (confirmation) {
            // Obtener el token CSRF de la cookie
            var csrftoken = getCookie('csrftoken');
            $.ajax({
                type: 'POST',
                
                url: 'user_delete2/' + userId + '/',
                dataType: 'json',
                success: function(response) {
                    if (response.success) {
                        alert('Usuario eliminado con éxito');
                        // Otra lógica aquí, como redirigir a otra página o actualizar la lista de usuarios
                    } else {
                        alert('Hubo un error al eliminar el usuario: ' + response.error);
                    }
                },
                error: function(xhr, errmsg, err) {
                    alert('Error al eliminar el usuario');
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        }
    });
});
// Función para obtener el token CSRF de la cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

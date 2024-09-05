$(document).ready(function() {
    $("#specialty").change(function(){
        $('#subSpecialty').empty()
        specialty = $('#specialty').val();
        $.ajax({
            url:  '/area/specialty_by_area/'+specialty,
            type:  'get',
            dataType:  'json',
            success: function(data) {
                data.specialty_kind.forEach(function(element) {
                    $('#subSpecialty').append('<option value="'+element.pk+'">'+ element.name +'</option>');
                    });
                }
            });

        })    

    });

function agregarItemYProducto() {
    // Obtener valores seleccionados o ingresados por el usuario
    let productoSeleccionado = document.getElementById('producto').value;
    let proveedorSeleccionado = document.getElementById('proveedor').value;
    let precioProducto = document.getElementById('producto').querySelector(`option[value="${productoSeleccionado}"]`).getAttribute('data-precio-producto');
    let nombreProducto = document.getElementById('producto').querySelector(`option[value="${productoSeleccionado}"]`).innerText;

    // Crear estructura de la nueva tabla a agregar
    let nuevaTabla = `
    <table>
        <thead>
            <tr>
                <th>Producto</th>
                <th>Precio</th>
                <th>Proveedor</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>${nombreProducto}</td>
                <td>${precioProducto}</td>
                <td>${proveedorSeleccionado}</td>
            </tr>
        </tbody>
    </table>
    `;

    // Agregar la nueva tabla al contenedor
    let contenedorTablas = document.getElementById('tablas-container');
    contenedorTablas.innerHTML += nuevaTabla;

    // Limpiar selección de producto después de agregarlo
    document.getElementById('producto').value = '';
}
    

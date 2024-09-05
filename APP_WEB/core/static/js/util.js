function volver() {
    history.back();
}
function agregarItemYProducto() {
    const productoSelect = document.getElementById('producto');
    const selectedOption = productoSelect.options[productoSelect.selectedIndex];
    const productoNombre = selectedOption.text;
    const productoPrecio = parseFloat(selectedOption.getAttribute('data-precio-producto'));

    if (!productoSelect.value) {
        alert('Seleccione un producto');
        return;
    }

    contadorItems++;
    const productosContainer = document.getElementById('productos-container');
    const nuevoProducto = document.createElement('div');
    nuevoProducto.classList.add('producto');
    nuevoProducto.innerHTML = `
        <input type="text" name="nombre[]" value="${productoNombre}" placeholder="Nombre del producto" required>
        <input type="number" name="cantidad[]" placeholder="Cantidad" required>
        <input type="number" name="precio[]" value="${productoPrecio}" placeholder="Precio" required>
        <input type="number" placeholder="Precio total" readonly>
        <button class="eliminarItem">Eliminar</button>
    `;

    productosContainer.appendChild(nuevoProducto);

    nuevoProducto.querySelector('input[placeholder="Cantidad"]').addEventListener('input', () => {
        const cantidad = parseFloat(nuevoProducto.querySelector('input[placeholder="Cantidad"]').value);
        const precioUnitario = parseFloat(productoPrecio);
        nuevoProducto.querySelector('input[placeholder="Precio total"]').value = (cantidad * precioUnitario).toFixed(2);
        actualizarTotal();
    });

    nuevoProducto.querySelector('.eliminarItem').addEventListener('click', () => {
        nuevoProducto.remove();
        actualizarTotal();
    });

    productoSelect.selectedIndex = 0;

    actualizarTotal();
}

function actualizarTotal() {
    const productos = document.querySelectorAll('.producto');
    let total = 0;
    productos.forEach(producto => {
        const cantidad = parseFloat(producto.querySelector('input[placeholder="Cantidad"]').value);
        const precioUnitario = parseFloat(producto.querySelector('input[name="precio[]"]').value);
        total += cantidad * precioUnitario;
    });
    document.getElementById('total').value = total.toFixed(2);
}


function enviar() {
    window.location.href = "URL_DE_ENVIO";
}


document.getElementById('agregarItem').addEventListener('click', agregarItemYProducto);
document.getElementById('volverButton').addEventListener('click', volver);
document.getElementById('enviarButton').addEventListener('click', enviar);

// Contenido de util.js

let today = new Date();

// Formatea la fecha como YYYY-MM-DD
let year = today.getFullYear();
let month = String(today.getMonth() + 1).padStart(2, '0');
let day = String(today.getDate()).padStart(2, '0');
let fecha_actual = `${year}-${month}-${day}`;

let contadorItems = 0;

function agregarItemYProducto() {
    const productoSelect = document.getElementById('producto');
    const selectedOption = productoSelect.options[productoSelect.selectedIndex];
    const productoNombre = selectedOption.text;
    const productoPrecio = parseFloat(selectedOption.getAttribute('data-precio-producto'));

    if (!productoSelect.value) {
        alert('Seleccione un producto');
        return;
    }

    contadorItems++;
    const productosContainer = document.getElementById('productos-container');
    const nuevoProducto = document.createElement('div');
    nuevoProducto.classList.add('producto');
    nuevoProducto.innerHTML = `
        <input type="text" name="nombre[]" value="${productoNombre}" placeholder="Nombre del producto" required>
        <input type="number" name="cantidad[]" placeholder="Cantidad" required>
        <input type="number" name="precio[]" value="${productoPrecio}" placeholder="Precio" required>
        <input type="number" placeholder="Precio total" readonly>
        <button class="eliminarItem">Eliminar</button>
    `;

    productosContainer.appendChild(nuevoProducto);

    nuevoProducto.querySelector('input[placeholder="Cantidad"]').addEventListener('input', () => {
        const cantidad = parseFloat(nuevoProducto.querySelector('input[placeholder="Cantidad"]').value);
        const precioUnitario = parseFloat(productoPrecio);
        nuevoProducto.querySelector('input[placeholder="Precio total"]').value = (cantidad * precioUnitario).toFixed(2);
        actualizarTotal();
    });

    nuevoProducto.querySelector('.eliminarItem').addEventListener('click', () => {
        nuevoProducto.remove();
        actualizarTotal();
    });

    productoSelect.selectedIndex = 0;

    actualizarTotal();
}

function cargarDatosYProductos(datos) {
    datos.forEach(dato => {
        contadorItems++;
        const productosContainer = document.getElementById('productos-container');
        const nuevoProducto = document.createElement('div');
        nuevoProducto.classList.add('producto');
        nuevoProducto.innerHTML = `
            <input type="text" name="nombre[]" value="${dato.nombre}" placeholder="Nombre del producto" required>
            <input type="number" name="cantidad[]" value="${dato.cantidad}" placeholder="Cantidad" required>
            <input type="number" name="precio[]" value="${dato.precio}" placeholder="Precio" required>
            <input type="number" value="${(dato.cantidad * dato.precio).toFixed(2)}" placeholder="Precio total" readonly>
            <button class="eliminarItem">Eliminar</button>
        `;

        productosContainer.appendChild(nuevoProducto);

        nuevoProducto.querySelector('input[placeholder="Cantidad"]').addEventListener('input', () => {
            const cantidad = parseFloat(nuevoProducto.querySelector('input[placeholder="Cantidad"]').value);
            const precioUnitario = parseFloat(dato.precio);
            nuevoProducto.querySelector('input[placeholder="Precio total"]').value = (cantidad * precioUnitario).toFixed(2);
            actualizarTotal();
        });

        nuevoProducto.querySelector('.eliminarItem').addEventListener('click', () => {
            nuevoProducto.remove();
            actualizarTotal();
        });
    });

    actualizarTotal();
}

function actualizarTotal() {
    const productos = document.querySelectorAll('.producto');
    let total = 0;
    productos.forEach(producto => {
        const cantidad = parseFloat(producto.querySelector('input[placeholder="Cantidad"]').value);
        const precioUnitario = parseFloat(producto.querySelector('input[name="precio[]"]').value);
        total += cantidad * precioUnitario;
    });
    document.getElementById('total').value = total.toFixed(2);
}

function volver() {
    history.back();
}

function enviar() {
    window.location.href = "URL_DE_ENVIO";
}

document.getElementById('agregarItem').addEventListener('click', agregarItemYProducto);

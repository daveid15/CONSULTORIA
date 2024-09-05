function agregarItemYProducto() {
    let productosContainer = document.getElementById('productos-container');
    let selectedProduct = document.getElementById('producto').value;
    let selectedProductText = document.getElementById('producto').selectedOptions[0].text;
    let precioProducto = document.getElementById('producto').selectedOptions[0].getAttribute('data-precio-producto');
    
    let tabla = document.getElementById('tabla-productos');
    let newRow = tabla.insertRow();
    
    let cell1 = newRow.insertCell(0);
    let cell2 = newRow.insertCell(1);
    let cell3 = newRow.insertCell(2);
    
    cell1.innerHTML = selectedProductText;
    cell2.innerHTML = precioProducto;
    cell3.innerHTML = `<button onclick="eliminarItem(this)">Eliminar</button>`;
    
    actualizarTotal(precioProducto);
}

function actualizarTotal(precioProducto) {
    let totalInput = document.getElementById('total');
    let total = parseFloat(totalInput.value) || 0;
    total += parseFloat(precioProducto);
    totalInput.value = total.toFixed(2);
}

function eliminarItem(button) {
    let row = button.parentNode.parentNode;
    let precioProducto = parseFloat(row.cells[1].innerText);
    row.parentNode.removeChild(row);
    
    actualizarTotal(-precioProducto);
}

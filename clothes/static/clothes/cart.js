
function actualizarCantidad(size_pk, accion) {
    // Crear objeto XMLHttpRequest para enviar solicitud AJAX
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/sales-cart", true); 
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}"); 

    // Al recibir respuesta, actualizar la interfaz
    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText); 
            var quantity = response.quantity;
            var total_price = response.total_price;
            var sum_prices = response.sum_prices;

            // Actualizar el precio total del ítem
            document.getElementById("total_price_" + size_pk).textContent = total_price.toFixed(2);

            // Actualizar la cantidad en el campo de entrada
            document.getElementById("cant_product_" + size_pk).value = quantity;

            // Actualizar el total general
            var sum_prices = 0;
            document.querySelectorAll(".total_price").forEach(function (el) {
                total_general += parseFloat(el.textContent);
            });
            document.getElementById("total_general").textContent = sum_prices.toFixed(2);
        }
      } 
    };

    // Enviar la solicitud POST con el ID de la talla y la acción a realizar
    var data = {
      'size_pk': size_pk,
      'accion': accion
    };
    
{
  xhr.send(JSON.stringify(data));;  

}
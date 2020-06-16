function realizarPeticion(ruta, nombreParam, valoresParam, mensaje){
    var xmlHTTP = new XMLHttpRequest();
    var url = ruta+"?";
    var cantidadParametros = nombreParam.length;
    for (var i = 0; i < cantidadParametros; i++){
        if(i == cantidadParametros - 1){
            url += nombreParam[i] + "=" + valoresParam[i];
        }
        else{
            url += nombreParam[i] + "=" + valoresParam[i] + "&";
        }
    }
    xmlHTTP.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var res = JSON.parse(this.responseText);
                console.log(res);
                alert(mensaje);//eliminar
                location.reload();
            }
    };
    xmlHTTP.open("GET", url, true);
    xmlHTTP.send();
}

function agregarAlCarrito(nombre, precio, cantidad, categoria){
    var nombreParam = ['nombre', 'precio','cantidad', 'categoria'];
    var valoresParam = [nombre, precio, cantidad, categoria];
    var url ="/agregarDetalle";
    realizarPeticion(url, nombreParam, valoresParam, "Agregado al carrito!");
}
function cambiarCantidad(id_detalle){
    console.log("he entrado");
    var cantidad = prompt("Ingrese la nueva cantidad: ");
    // validar cantidad sea nulo

    var nombreParam = ['idDetalleCarrito','cantidad'];
    var valoresParam = [id_detalle, cantidad];
    var url ="/cambiarCantidad";
    realizarPeticion(url, nombreParam, valoresParam, "Cantidad modificada!");
}

function comprar(){
    realizarPeticion("/comprar", [], [], "Compra realizada!");
}
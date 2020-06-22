function realizarPeticion(ruta, nombreParam, valoresParam, mensaje, isReload){
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
                if(isReload){
                    location.reload();
                }

            }
    };
    xmlHTTP.open("GET", url, true);
    xmlHTTP.send();
}

function agregarAlCarrito(nombre, precio, idInput, categoria){

    var cantidad = document.getElementById(idInput).value;
    var nombreParam = ['nombre', 'precio','cantidad', 'categoria'];
    var valoresParam = [nombre, precio, cantidad, categoria];
    var url ="/agregarDetalle";
    realizarPeticion(url, nombreParam, valoresParam, "Agregado al carrito!", false);
}
function cambiarCantidad(id_detalle, IdInput){

    var cantidad = document.getElementById(IdInput).value;
        // validar cantidad sea nulo
    if(cantidad > 0){

        var nombreParam = ['idDetalleCarrito','cantidad'];
        var valoresParam = [id_detalle, cantidad];
        var url ="/cambiarCantidad";
        realizarPeticion(url, nombreParam, valoresParam, "Cantidad modificada!", true);

    }
}

function comprar(){
    realizarPeticion("/comprar", [], [], "Compra realizada!", true);
}

function elminarProducto(id_detalle){
    console.log("he entrado");
    var nombreParam = ['idDetalleCarrito'];
    var valoresParam = [id_detalle];
    var url ="/eliminarProducto";
    realizarPeticion(url, nombreParam, valoresParam,  "Producto Eliminado!", true)

}
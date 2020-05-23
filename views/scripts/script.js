/*Función que muestra el formulario para registro*/
function mostrarRegistro()
{
    /*Cambio la propiedad visibility a visible para que el formulario se muestre*/
    document.getElementById("login").style.display = "none"
    document.getElementById("regForm").style.visibility = "visible"
    document.getElementById("regForm").style.display = "inline"

}

function mostrarComentario(id)
{
    if (document.getElementsByClassName("comentarPublicacion")[id].style.display == "none")
        document.getElementsByClassName("comentarPublicacion")[id].style.display = "block"
    else
        document.getElementsByClassName("comentarPublicacion")[id].style.display = "none"
}
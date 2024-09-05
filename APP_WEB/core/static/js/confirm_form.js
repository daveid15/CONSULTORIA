
$('#form_confirm').submit(function() {
    var cont_select = $('#type_close').val();
    if (cont_select == ''){
        alert("no ha seleccionado ninguna opción")
        return false
        }
    else{    
        if ((cont_select == 'Finaliza solo esta reunión') || (cont_select == 'Finaliza la reunión y la asesoría') || (cont_select == 'Solicita revisión')){
            var msj = 'Usted escogio la opción "'+cont_select+'", presione confirmar para continuar de lo contrario presione cancelar';
            var ok = confirm(msj);
            return ok; 
            }
        else{
            alert("La opción seleccionada no corresponde")
            return false
            }
        }
    });

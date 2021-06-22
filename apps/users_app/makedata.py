from apps.users_app.models import UserType, Lawsuit_State, Court


def make_user_type():
    all_users_type = UserType.objects.all() #resetea los datos
    all_users_type.delete()
    secretaria = UserType.objects.create(type_name = "secretaria")
    procuradora = UserType.objects.create(type_name = "procuradora")


def make_lawsuit_state():
    all_lawsuit_states = Lawsuit_State.objects.all() #resetea los datos
    all_lawsuit_states.delete()

    Lawsuit_State.objects.create(name_state = "escritura creada") #secretaria
    Lawsuit_State.objects.create(name_state = "caratula asignada") #secretaria
    Lawsuit_State.objects.create(name_state = "despachese mandamiento") #secretaria

    Lawsuit_State.objects.create(name_state = "demanda proveida") #procuradora, una vez el juez aprueba tras haber revisado el pagaré original
    Lawsuit_State.objects.create(name_state = "solicita notificacion demandado") #procuradora, solicita a receptor judicial notificar al demandado
    Lawsuit_State.objects.create(name_state = "solicita traba de bienes") #procuradora, solicita a receptor judicial notificar al demandado
    Lawsuit_State.objects.create(name_state = "solicita fuerza publica") #procuradora, solicita a receptor judicial notificar al demandado
    Lawsuit_State.objects.create(name_state = "lanzamieno de bienes") #procuradora, retiro de bienes
    Lawsuit_State.objects.create(name_state = "termino con recuperacion") #procuradora, el retiro de los bienes fueron suficiente para cerrar la causa
    Lawsuit_State.objects.create(name_state = "termino sin recuperacion") #procuradora, no se encontraron bienes embargables, (insolvencia)
    Lawsuit_State.objects.create(name_state = "termino con advenimiento") #procuradora, se llegó a un acuerdo con el demandado(repactación o se pagó la totalidad de la deuda)


def make_court():
    all_court = Court.objects.all() #resetea los datos
    all_court.delete()
    Court.objects.create(name_court = "no asignado" , comuna = "no asignado", cod_tribunal= "00")
    Court.objects.create(name_court = "1° Juzgado de Letras de La Serena" , comuna = "La Serena" , cod_tribunal= "40")
    Court.objects.create(name_court = "2° Juzgado de Letras de La Serena" , comuna = "La Serena", cod_tribunal= "41")
    Court.objects.create(name_court = "3° Juzgado de Letras de La Serena" , comuna = "La Serena", cod_tribunal= "42")
    Court.objects.create(name_court = "1° Juzgado de Letras de Coquimbo" , comuna = "Coquimbo" , cod_tribunal= "43" )
    Court.objects.create(name_court = "2° Juzgado de Letras de Coquimbo" , comuna = "Coquimbo", cod_tribunal= "44")
    Court.objects.create(name_court = "3° Juzgado de Letras de Coquimbo" , comuna = "Coquimbo", cod_tribunal= "45")
    Court.objects.create(name_court = "Juzgado de Letras de Vicuña" , comuna = "Vicuña",  cod_tribunal= "46")
    Court.objects.create(name_court = "Juzgado de Letras y garantía de Andacollo" , comuna = "Andacollo", cod_tribunal= "47")
    Court.objects.create(name_court = "1° Juzgado de Letras de Ovalle" , comuna = "Ovalle", cod_tribunal= "48")
    Court.objects.create(name_court = "2° Juzgado de Letras de Ovalle" , comuna = "Ovalle", cod_tribunal= "49")
    Court.objects.create(name_court = "3° Juzgado de Letras de Ovalle" , comuna = "Ovalle", cod_tribunal= "50")
    Court.objects.create(name_court = "Juzgado de Letras y Gar. de Combarbalá" , comuna = "Combarbalá", cod_tribunal= "51")
    Court.objects.create(name_court = "Juzgado de Letras de Illapel" , comuna = "Illapel", cod_tribunal= "52")
    Court.objects.create(name_court = "Juzgado de Letras y Gar. de los Vilos" , comuna = "Los Vilos", cod_tribunal= "53")




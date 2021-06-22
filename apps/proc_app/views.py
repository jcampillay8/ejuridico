from django.shortcuts import render, redirect
from apps.users_app.models import Administrator, Court, Lawsuit_State, User, UserType
from apps.users_app.models import    Lawsuit, Defendant, LawsuitHistory
from django.db.models.query_utils import Q
from apps.proc_app.forms.new_movement import NewMovementForm2, DocumentForm

# Create your views here.
def index(request):
    if not 'id' in request.session or request.session['user_type'] != "procuradora":
        return redirect('/')
    this_user= User.objects.get(id = int(request.session['id'])) 
    all_lawsuits = Lawsuit.objects.all()
    all_defendants = Defendant.objects.all()
    all_pending_lawsuits = Lawsuit.objects.exclude(current_demand_state__name_state__in = ["caratula asignada", "escritura creada"])


    context = {
        'this_user' : this_user,
        'all_lawsuits' : all_lawsuits,
        'all_defendants' : all_defendants,
        'all_pending_lawsuits' : all_pending_lawsuits,
    }
    return render(request,'dashboard_procuradora.html', context)


def lawsuit_detail(request, id_lawsuit):
    if not 'id' in request.session or request.session['user_type'] != "procuradora":
        return redirect('/')
    this_user = User.objects.get(id = int(request.session['id'])) 
    this_lawsuit = Lawsuit.objects.get(id= id_lawsuit)
    this_defendant = this_lawsuit.current_defendant
    this_lawsuit_history = this_lawsuit.lawsuit_history
    # new_movement_form = NewMovementForm()
    print(this_lawsuit.current_demand_state.name_state)
   
    if this_lawsuit.current_demand_state.name_state == "caratula asignada" or this_lawsuit.current_demand_state.name_state == "escritura creada":
        context = {
            'this_user' : this_user,
            'this_lawsuit' : this_lawsuit,
            'this_defendant' : this_defendant,
            'this_lawsuit_history' : this_lawsuit_history,
            'hidden' : "hidden" #esconder el boton 
                }

    else:
        document_form = DocumentForm()
        current_state = this_lawsuit.current_demand_state
        new_movement_form = NewMovementForm2(initial= {'current_demand_state': current_state}) 
        context = {
            'this_user' : this_user,
            'this_lawsuit' : this_lawsuit,
            'this_defendant' : this_defendant,
            'this_lawsuit_history' : this_lawsuit_history,
            'new_movement_form' : new_movement_form,
            'document_form' : document_form,
            'hidden' : " " #NO esconder el boton 

            }       
    return render(request, "lawsuit_detail2.html", context)

def update_lawsuit_state(request, id_lawsuit):
    if not 'id' in request.session or request.session['user_type'] != "procuradora":
        return redirect('/')

    this_user = User.objects.get(id = int(request.session['id'])) 
    this_lawsuit = Lawsuit.objects.get(id= id_lawsuit)
    past_state = this_lawsuit.current_demand_state
    
    
    new_state_id = request.POST['current_demand_state']
    new_state = Lawsuit_State.objects.get(id = int(new_state_id))

    

    if NewMovementForm2(request.POST).is_valid and DocumentForm(request.POST, request.FILES).is_valid:
        print("cambio es valido "*20)
        this_lawsuit.current_demand_state = new_state
        this_lawsuit.save(update_fields = ['current_demand_state'])
        new_history  = LawsuitHistory.objects.create(          #generar el cambio en el historial de la demanda
                lawsuit_associate = this_lawsuit, #estado primera creación
                past_state = past_state, #estado primera creación
                current_state = this_lawsuit.current_demand_state,
                change_made_by = this_user,
                docfile=request.FILES['docfile'],

            )



    else:
        print("cambio NO valido"*20)
    document_form = DocumentForm()
    this_defendant = this_lawsuit.current_defendant
    this_lawsuit_history = this_lawsuit.lawsuit_history
    current_state = this_lawsuit.current_demand_state
    new_movement_form = NewMovementForm2(initial= {'current_demand_state': current_state})
    context = {
        'this_user' : this_user,
        'this_lawsuit' : this_lawsuit,
        'this_defendant' : this_defendant,
        'this_lawsuit_history' : this_lawsuit_history,
        'new_movement_form' : new_movement_form,
        'document_form' : document_form,
        

    }
    return render(request, "lawsuit_detail2.html", context)
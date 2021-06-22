import re
from django.db.models.query_utils import Q
from apps.users_app.models import Administrator, Court, Lawsuit_State, User, UserType
from django.shortcuts import redirect, render
from apps.users_app.forms.register import UserForm
from .forms.new_lawsuit import LawsuitForm, DefendantForm
from apps.secr_app.forms.new_movement import NewMovementForm, DocumentForm, AddCourt
from apps.users_app.models import    Lawsuit, Defendant, LawsuitHistory
from .utils import render_to_pdf
from django.http import HttpResponse
from django.forms import ModelChoiceField


# import webbrowser
# 

def index(request):
    if not 'id' in request.session or request.session['user_type'] != "secretaria":
        return redirect('/')
    this_user= User.objects.get(id = int(request.session['id'])) 
    all_pending_lawsuits = Lawsuit.objects.filter(current_demand_state__name_state__in = ["caratula asignada", "escritura creada"]) #las tareas pendientes son los estados carátula asiganda y escritura creada
    all_lawsuits = Lawsuit.objects.all()
    all_defendants = Defendant.objects.all()


    context = {
        'this_user' : this_user,
        'all_lawsuits' : all_lawsuits,
        'all_pending_lawsuits' : all_pending_lawsuits,
        'all_defendants' : all_defendants,
    }
    return render(request, 'dashboard_secretary.html', context)


def create_lawsuit(request):
    if not 'id' in request.session or request.session['user_type'] != "secretaria":
        return redirect('/')
    this_user= User.objects.get(id = int(request.session['id'])) 
    if request.method == 'GET':
        defendantform = DefendantForm()
        lawsuitform = LawsuitForm()
        context = {
        'defendantform' : defendantform,
        'lawsuitform' : lawsuitform,
            }
        return render(request, 'new_lawsuit.html',context)
    else: #si es post
        lawsuitform = LawsuitForm(request.POST)
        defendantform = DefendantForm(request.POST)

        if defendantform.is_valid() and lawsuitform.is_valid():
            print("ES valido"*10)

            new_defendant = defendantform.save(commit=False) #guarda al demandado
            new_defendant.defendant_created_by = this_user 
            new_defendant.save()

            new_lawsuit = lawsuitform.save(commit=False)
            new_lawsuit.current_court = Court.objects.get(cod_tribunal = "00")
            new_lawsuit.current_demand_state = Lawsuit_State.objects.get(name_state = "escritura creada")
            new_lawsuit.current_defendant = new_defendant
            new_lawsuit.lawsuit_created_by = this_user
            new_lawsuit.save()

            new_history  = LawsuitHistory.objects.create(
                lawsuit_associate = new_lawsuit, #estado primera creación
                past_state = new_lawsuit.current_demand_state, #estado primera creación
                current_state = new_lawsuit.current_demand_state,
                change_made_by = this_user,

            )



            context = {
                # 'first_name1' : new_defendant.first_name1,
                # 'first_name2' : new_defendant.first_name2,
                # 'last_name1' : new_defendant.last_name1,
                # 'last_name2' : new_defendant.last_name2,
                # 'address' : new_defendant.address,
                # 'rut' : new_defendant.rut,

                # 'new_lawsuit' : new_lawsuit.num_promissory_notes,
                # 'rut' : new_lawsuit.final_date,
                # 'rut' : new_lawsuit.rut,
                'defendant' : new_defendant,
                'lawsuit' : new_lawsuit,

            }

            pdf = render_to_pdf('lawsuitpdf.html', context)
            # response = "escrito%s.pdf" %("new_defendant.first_name")
            # webbrowser.open_new('/') 
            redirect('/')
            return  HttpResponse(pdf, content_type='application/pdf')
            # return render(request, 'lawsuitpdf.html',context)

        # si no es válido
        print("no es valido"*10)
        context = {
            'defendantform' : defendantform,
            'lawsuitform' : lawsuitform,
        }
        return render(request, 'new_lawsuit.html',context)

def lawsuit_detail(request, id_lawsuit):
    if not 'id' in request.session or request.session['user_type'] != "secretaria":
        return redirect('/')
    this_user = User.objects.get(id = int(request.session['id'])) 
    this_lawsuit = Lawsuit.objects.get(id= id_lawsuit)
    this_defendant = this_lawsuit.current_defendant
    this_lawsuit_history = this_lawsuit.lawsuit_history
    # query_set = Lawsuit.objects.filter(current_demand_state__name_state__in = ["caratula asignada", "escritura creada"])
    document_form = DocumentForm()
    # new_movement_form = NewMovementForm()
    
    current_state = this_lawsuit.current_demand_state
    current_court = this_lawsuit.current_court
    new_movement_form = NewMovementForm(initial= {'current_demand_state': current_state})
    add_court_form = AddCourt(initial= {'current_court': current_court})
   
    print(new_movement_form)
    context = {
        'this_user' : this_user,
        'this_lawsuit' : this_lawsuit,
        'this_defendant' : this_defendant,
        'this_lawsuit_history' : this_lawsuit_history,
        'new_movement_form' : new_movement_form,
        'document_form' : document_form,
        'add_court_form' : add_court_form,
        

    }
    return render(request, "lawsuit_detail.html", context)

def re_make_lawsuitpdf(request, id_lawsuit):
    if not 'id' in request.session or request.session['user_type'] != "secretaria":
        return redirect('/')
    this_user = User.objects.get(id = int(request.session['id'])) 
    this_lawsuit = Lawsuit.objects.get(id= id_lawsuit)
    this_defendant = this_lawsuit.current_defendant

   
    context = {

                'defendant' : this_defendant,
                'lawsuit' : this_lawsuit,

    }
    pdf = render_to_pdf('lawsuitpdf.html', context)
    return  HttpResponse(pdf, content_type='application/pdf') 



def update_lawsuit_state(request, id_lawsuit):
    if not 'id' in request.session or request.session['user_type'] != "secretaria":
        return redirect('/')

    this_user = User.objects.get(id = int(request.session['id'])) 
    this_lawsuit = Lawsuit.objects.get(id= id_lawsuit)
    past_state = this_lawsuit.current_demand_state
    
    
    new_state_id = request.POST['current_demand_state']
    new_state = Lawsuit_State.objects.get(id = int(new_state_id))

    

    if NewMovementForm(request.POST).is_valid and DocumentForm(request.POST, request.FILES).is_valid:
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
    new_movement_form = NewMovementForm(initial= {'current_demand_state': current_state})
    context = {
        'this_user' : this_user,
        'this_lawsuit' : this_lawsuit,
        'this_defendant' : this_defendant,
        'this_lawsuit_history' : this_lawsuit_history,
        'new_movement_form' : new_movement_form,
        'document_form' : document_form,
        

    }

    return render(request, "lawsuit_detail.html", context)

def update_lawsuit_court(request, id_lawsuit):
    if not 'id' in request.session or request.session['user_type'] != "secretaria":
        return redirect('/')
    this_user = User.objects.get(id = int(request.session['id']))
    this_lawsuit = Lawsuit.objects.get(id= id_lawsuit)
    past_state = this_lawsuit.current_demand_state #estado antiguo de la demanda
    add_court_form = AddCourt(request.POST)
    print(request.POST['current_court'])
    if add_court_form.is_valid():
        this_lawsuit.cause_rol = request.POST['cause_rol']
        this_lawsuit.current_demand_state = Lawsuit_State.objects.get(name_state = "caratula asignada")
        this_lawsuit.current_court = Court.objects.get(id = request.POST['current_court'])

        this_lawsuit.save(update_fields = ['cause_rol','current_demand_state','current_court'])
       
        new_history  = LawsuitHistory.objects.create(          #generar el cambio en el historial de la demanda
            lawsuit_associate = this_lawsuit, 
            past_state = past_state, #estado primera creación
            current_state = this_lawsuit.current_demand_state,
            change_made_by = this_user,
                )
    document_form = DocumentForm()
    current_state = this_lawsuit.current_demand_state           
    new_movement_form = NewMovementForm()
    this_defendant = this_lawsuit.current_defendant
    this_lawsuit_history = this_lawsuit.lawsuit_history
    context = {
        'this_user' : this_user,
        'this_lawsuit' : this_lawsuit,
        'this_defendant' : this_defendant,
        'this_lawsuit_history' : this_lawsuit_history,
        'new_movement_form' : new_movement_form,
        'document_form' : document_form,
        'add_court_form' : add_court_form,
        

    }

    return render(request, "lawsuit_detail.html", context)



    


    





def delete_lawsuit(request, id_lawsuit):
    if not 'id' in request.session or request.session['user_type'] != "secretaria":
        return redirect('/')
    this_lawsuit = Lawsuit.objects.get(id = id_lawsuit )
    print(f"se borrarla la demanda id = {this_lawsuit.id}")
    this_lawsuit.delete()
    return redirect('/')


# def make_lawsuit_document(request, lawsuitform):

#     pass

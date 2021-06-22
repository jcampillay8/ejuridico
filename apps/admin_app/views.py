from apps.users_app.models import Administrator, User, UserType
from django.shortcuts import redirect, render
from apps.users_app.forms.register import UserForm

# Create your views here.


def administrator_dashbord(request):
    if not 'id' in request.session or request.session['user_type'] != "administrator":
        return redirect('/')
    this_administrator = Administrator.objects.get(id = int(request.session['id'])) 
    all_users = User.objects.all()
    context = {
        'this_administrator' : this_administrator,
        'all_users' : all_users,
    }
    return render(request, 'administratordashboard.html', context)



def new_user(request):
    if not 'id' in request.session or request.session['user_type'] != "administrator":
        return redirect('/')

    if request.method == 'GET':

        userform = UserForm()
        context = {
            'userform' : userform
        }
        return render(request, 'new_user.html', context)
    
    #si es post
    userform = UserForm(request.POST)
    this_administrator = Administrator.objects.get(id = int(request.session['id']))
    if userform.is_valid():
        
        new_user = userform.save(commit=False) #lo que se guarda desde el form
        new_user.users_created_by = this_administrator # lo que se asigna desde el views
        new_user.save()
        print(f"usuario creado")
        return redirect('/')

    context = {
        'userform' : userform,
        'this_administrator' : this_administrator,
    }
    return render(request, 'new_user.html', context)




def delete_user(request, user_id):
    if not 'id' in request.session or request.session['user_type'] != "administrator":
        return redirect('/')

    if request.method == 'GET':
        user_to_delete = User.objects.get(id = user_id)
        print(f"ID usuario a borrar {user_to_delete.id} se llama {user_to_delete.first_name1} {user_to_delete.last_name1}")
        user_to_delete.delete()
        return redirect('/')

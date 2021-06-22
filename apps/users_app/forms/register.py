from django.db.models import query
from django.forms import ModelForm
from django import forms
from apps.users_app.models import Administrator, User, UserType



class AdministratorForm(ModelForm):
        confirm_password=forms.CharField(widget=forms.PasswordInput(attrs = {"class":"form-control"}), label='Confirme su contraseña')
        class Meta:
                model = Administrator 
                fields = ['first_name1','first_name2','last_name1','last_name2','rut','email', 'password']
                widgets = {
                'first_name1': forms.TextInput(attrs = {"class":"form-control "}),
                'first_name2': forms.TextInput(attrs = {"class":"form-control "}),
                'last_name1': forms.TextInput(attrs = {"class":"form-control "}),
                'last_name2': forms.TextInput(attrs = {"class":"form-control "}),
                'rut': forms.TextInput(attrs = {"class":"form-control "}),
                'email': forms.TextInput(attrs = {"class":"form-control "}),
                'password' : forms.PasswordInput(attrs = {"class":"form-control "}),

                }
                labels = {
                        'first_name1': 'Nombre:',
                        'first_name2': 'Segundo Nombre:',
                        'last_name1': 'Apellido paterno:',
                        'last_name2': 'Apellido Materno:',
                        'rut': 'Rut:',
                        'email': 'Email:',
                        'password': 'Contraseña:',
                }



class UserForm(ModelForm):

 

        class Meta:
                model = User 
                fields = ['first_name1','first_name2','last_name1','last_name2','rut','type','email', 'password']
                typea = forms.ModelChoiceField(queryset=UserType.objects.all(), required=False, help_text="Company")

                widgets = {
                        'first_name1': forms.TextInput(attrs = {"class":"form-control "}),
                        'first_name2': forms.TextInput(attrs = {"class":"form-control "}),
                        'last_name1': forms.TextInput(attrs = {"class":"form-control "}),
                        'last_name2': forms.TextInput(attrs = {"class":"form-control "}),
                        'type': forms.Select( attrs = {"class":"form-control "},),
                        'rut': forms.TextInput(attrs = {"class":"form-control", "id": "rut", "onkeypress":"isInputNumber(event)"}),
                        'email': forms.TextInput(attrs = {"class":"form-control "}),
                        'password' : forms.PasswordInput(attrs = {"class":"form-control "}),

                        }

                labels = {
                        'first_name1': 'Nombre:',
                        'first_name2': 'Segundo Nombre:',
                        'last_name1': 'Apellido paterno:',
                        'last_name2': 'Apellido materno:',
                        'rut': 'Rut:',
                        'type': 'Tipo de usuario:',
                        'email': 'Email:',
                        'password': 'Contraseña:',
                }



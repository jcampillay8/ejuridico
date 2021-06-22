from django.db.models.base import Model
from django import forms
from django.forms import ModelForm
from apps.users_app.models import Defendant
from apps.users_app.models import Lawsuit

class DefendantForm(ModelForm):
    class Meta:
        model = Defendant
        fields = ['first_name1','first_name2','last_name1','last_name2','rut','address']
        #widgets = {
            #'first_name1': forms.Textarea(attrs = {"class":"form-control ", "rows":4, "cols": "50%" , "style":"resize: none;"})}
# , "onkeypress":"isInputNumber(event)



        widgets = {
            'first_name1': forms.TextInput(attrs = {"class":"form-control "}),
            'first_name2': forms.TextInput(attrs = {"class":"form-control "}),
            'last_name1': forms.TextInput(attrs = {"class":"form-control "}),
            'last_name2': forms.TextInput(attrs = {"class":"form-control "}),
        
            'rut': forms.TextInput(attrs = {"class":"form-control", "id": "rut", "onkeypress":"isInputNumber(event)"}),
            'address': forms.TextInput(attrs = {"class":"form-control "}),

            }

        labels = {
                'first_name1': 'Primer Nombre',
                'first_name2': 'Segundo Nombre',
                'last_name1': 'Primer Apellido',
                'last_name2': 'Segundo Apellido',
                'rut': 'RUT',
                'address': 'Dirección Completa',
        }

class LawsuitForm(ModelForm):
    class Meta:
        model = Lawsuit
        fields = ['num_promissory_notes','final_date','mount_to_pay','num_operation','suscription_date','demand_amount']

        widgets = {
            'num_promissory_notes': forms.TextInput(attrs = {"class":"form-control", 'autocomplete' : 'off'}),
            'final_date': forms.DateInput(attrs = {"class":"form-control", "type":"date", 'autocomplete' : 'off', 'input_format' : "%Y/%m/%d"}),
            'mount_to_pay': forms.TextInput(attrs = {"class":"form-control", 'autocomplete' : 'off', "onkeypress":"isInputNumber(event)", "id": "monto1"}),
            'num_operation': forms.TextInput(attrs = {"class":"form-control", 'autocomplete' : 'off'}),
            'suscription_date': forms.DateInput(attrs = {"class":"form-control", "type":"date", 'autocomplete' : 'off', 'input_format' : "%Y/%m/%d"}),
            'demand_amount': forms.TextInput(attrs = {"class":"form-control", 'autocomplete' : 'off', "onkeypress":"isInputNumber(event)", "id": "monto2"}),
            }

        labels ={
            'num_promissory_notes':'Número Pagaré',
            'final_date': 'Fecha MORA',
            'mount_to_pay': 'Monto pagaré',
            'num_operation':'Número de Operación',
            'suscription_date':'Fecha Suscripción',
            'demand_amount':'Cuantía de la demanda',
        }

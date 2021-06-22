from django import forms
from django.db.models import query
from django.forms import ModelForm
from apps.users_app.models import Lawsuit, LawsuitHistory, Lawsuit_State, Court


class NewMovementForm(ModelForm):
    class Meta:
        model = Lawsuit
        fields = ['current_demand_state']

        widgets = {
            
            'current_demand_state': forms.Select( attrs = {"class":"form-control "}),


            }

        labels = {
                'current_demand_state': 'Cambiar de estado a:',

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['current_demand_state'].queryset = Lawsuit.objects.filter(current_demand_state__name_state__in = ["caratula asignada", "escritura creada"])
        self.fields['current_demand_state'].queryset = Lawsuit_State.objects.filter(name_state__in = ["despachese mandamiento"])


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Seleccione el documento')
# quedé acá-----------------------------------------------------
class AddCourt(ModelForm):
    class Meta:
        model = Lawsuit
        fields = ['cause_rol','current_court']
        widgets = {
            'cause_rol': forms.TextInput(attrs = {"class":"form-control", 'autocomplete' : 'off'}),
            'current_court': forms.Select( attrs = {"class":"form-control" }),
            }
            
        labels = {
                'cause_rol' : 'Causa Rol',
                'current_court': 'Asignar Tribunal:',

        }


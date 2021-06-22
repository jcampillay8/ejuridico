from django import forms
from django.db.models import query
from django.forms import ModelForm
from apps.users_app.models import Lawsuit, LawsuitHistory, Lawsuit_State


class NewMovementForm2(ModelForm):
    class Meta:
        model = Lawsuit
        fields = ['current_demand_state']
        print(fields)

        widgets = {
            'current_demand_state': forms.Select( attrs = {"class":"form-control "},),
            }

        labels = {
                'current_demand_state': 'Cambiar de estado:',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['current_demand_state'].queryset = Lawsuit.objects.filter(current_demand_state__name_state__in = ["caratula asignada", "escritura creada"])
        self.fields['current_demand_state'].queryset = Lawsuit_State.objects.exclude(name_state__in = ["caratula asignada", "escritura creada", "despachese mandamiento"])


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Seleccione el documento')
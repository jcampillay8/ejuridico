from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django import forms
import re

from datetime import date, datetime, timedelta

# Create your models here.



def ValidarLongitudPassword(cadena):
    if len(cadena) < 8:
        raise forms.ValidationError(
            f'Error: la contraseña al menos debe contener 8 caracteres'
        )



def validarEmail(cadena):
    #valida que el email tenga el formato correcto
    EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if not EMAIL_REGEX.match(cadena):          
        raise forms.ValidationError(
            f'Error de formato: {cadena} no es un e-mail valido'
        )
    #valida que el email no se repita
    
    for s in Administrator.objects.all():
            # se usa .lower() para ovbiar las mayúsculas en la comparación de palabras
            if cadena.lower() == s.email.lower(): 
                raise forms.ValidationError(
                f'Error: el email {cadena} ya existe en nuestros registros!'
                )




class Administrator(models.Model): #super usuario que crea o elimina User (hay que hacer formulario!!!!)
    first_name1 = models.CharField(max_length=45, blank=False, null=False)
    first_name2 = models.CharField(max_length=45, blank=False, null=False)
    last_name1 = models.CharField(max_length=45, blank=False, null=False)
    last_name2 = models.CharField(max_length=45, blank=False, null=False)
    rut = models.CharField(max_length=20, blank=False, null=False)
    email = models.CharField(max_length=30, blank=False, null=False, validators=[validarEmail])
    password = models.CharField(max_length=100, validators=[ValidarLongitudPassword])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Administrator, self).save(*args, **kwargs)

    @staticmethod
    def authenticate(email, password):
        admin = Administrator.objects.filter(email = email)
        print ('user', admin)
        #buscar si hay un email en la base de datos
        if len(admin) == 1:
            #si existe un email asociado
            #se existe un el usuario (se supone que debe ser uno solo por sus validaciones)
            admin = admin[0]
            bd_password = admin.password
            if check_password(password, bd_password): #convierte los hash y los comparas
                return admin

        return None 

class UserType(models.Model):
    type_name = models.CharField(max_length=50, blank=False, null=False) #secretaria, abogado, o procuradora
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.type_name



class User(models.Model):
    first_name1 = models.CharField(max_length=45, blank=False, null=False)
    first_name2 = models.CharField(max_length=45, blank=False, null=False)
    last_name1 = models.CharField(max_length=45, blank=False, null=False)
    last_name2 = models.CharField(max_length=45, blank=False, null=False)
    rut = models.CharField(max_length=12, blank=False, null=False)
    email = models.CharField(max_length=30, blank=False, null=False, validators=[validarEmail])
    password = models.CharField(max_length=100, validators=[ValidarLongitudPassword])

    type = models.ForeignKey(UserType, related_name="type_user", on_delete = models.CASCADE)
    users_created_by = models.ForeignKey(Administrator, related_name="administrator_create", on_delete = models.CASCADE)
    # user_manage_lawsuit = models.ManyToManyField(Lawsuit, related_name="lawsuit_managed_by")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    @staticmethod
    def authenticate(email, password):
        user = User.objects.filter(email = email)
        print ('user', user)
        #buscar si hay un email en la base de datos
        if len(user) == 1:
            #si existe un email asociado
            #se existe un el usuario (se supone que debe ser uno solo por sus validaciones)
            user = user[0]
            bd_password = user.password
            if check_password(password, bd_password): #convierte los hash y los comparas
                return user
        
        
        return None 



def ValidarLongitud(cadena):
    if len(cadena) < 2:
        raise forms.ValidationError(
            f'Error: Debe contener mínimo 3 caracteres'
        )
def ValidarRut(valor):
    rut_sincaracter = valor.replace("-", "").replace(".", "").replace(",", "")
    dv_ingresado = valor[-1]
    print(dv_ingresado)
    value = 11 - sum([ int(a)*int(b)  for a,b in zip(str(rut_sincaracter).zfill(9), '32765432')])%11
    dv_calculado = {10: 'K',10: 'k', 11: '0'}.get(value, str(value))
    print(dv_calculado)
    if dv_ingresado == dv_calculado :
        print("esta correcto")
        return 
    else :
        print("es incorrecto")
        raise forms.ValidationError(
        f'Error de RUT: rut inválido, favor verifique')        




# def Validar_Num_Pagare(pagare):

def Validar_Fecha(fecha_final):
    # DATE_REGEX = re.compile(r'^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))')
    # if not DATE_REGEX.match(fecha_final):
    #     raise forms.ValidationError(
    #         f'Error de formato: {fecha_final} debe tener el siguiente formato dd-mm-aaaa'
    #     )
    if fecha_final >= date.today():
        raise forms.ValidationError(
            f'Error fecha: {fecha_final} no puede estar en el futuro'
        )

def Validar_Monto_a_Pagar(monto_a_pagar):
    MONTO_REGEX = re.compile(r"[+-]?\d+(?:\.\d+)?")
    if not MONTO_REGEX.match(monto_a_pagar):
        raise forms.ValidationError(
            f'Error de formato: {monto_a_pagar} debe ser un numero valido'
        )        


# def Validar_Fecha_Suscripcion(fecha_suscripcion):
    # DATE_REGEX = re.compile(r'^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))')
    # if not DATE_REGEX.match(fecha_suscripcion):
    #     raise forms.ValidationError(
    #         f'Error de formato: {fecha_suscripcion} debe tener el siguiente formato dd-mm-aaaa'
    #     )
    # if fecha_suscripcion >= datetime.datetime.now():
    #     raise forms.ValidationError(
    #         f'Error fecha: {fecha_suscripcion} no puede estar en el futuro'
    #     )

def Validar_Monto_Demandado(monto_demandado):
    # MONTO_REGEX = re.compile(r"[+-]?\d+(?:\.\d+)?")

    # if not MONTO_REGEX.match(monto_demandado):
    #     raise forms.ValidationError(
    #         f'Error de formato: {monto_demandado} debser un numero valido'
    #     )  
    pass


class Lawsuit_State(models.Model):
    name_state = models.CharField(max_length=45, default="escritura creada")
    # demand_state = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name_state

class Court(models.Model):
    cod_tribunal = models.CharField(max_length=6, default="00")
    name_court = models.CharField(max_length=45, default="no asigando")
    comuna = models.CharField(max_length=45, default="no asigando")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name_court

class Defendant(models.Model): 
    first_name1 = models.CharField(max_length=45, blank=False, null=False, validators=[ValidarLongitud]) #este campo
    first_name2 = models.CharField(max_length=45, blank=False, null=False, validators=[ValidarLongitud]) #este campo
    last_name1 = models.CharField(max_length=45, blank=False, null=False, validators=[ValidarLongitud]) #este campo
    last_name2 = models.CharField(max_length=45, blank=False, null=False, validators=[ValidarLongitud]) #este campo
    address = models.CharField(max_length=255, blank=False, null=False,validators=[ValidarLongitud]) #este campo
    rut = models.CharField(max_length=25, blank=False, null=False,validators=[ValidarRut]) 

    defendant_created_by = models.ForeignKey(User, related_name="user_create_defendant", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Lawsuit(models.Model):
    num_promissory_notes = models.CharField(max_length=45,blank=False, null=False)   #este campo
    final_date = models.DateField(validators=[Validar_Fecha])  #este campo
    mount_to_pay = models.CharField(max_length=255, validators=[Validar_Monto_a_Pagar]) #este campo
    num_operation = models.CharField(max_length=255, blank=False, null=False) #este campo
    suscription_date= models.DateField(validators=[Validar_Fecha]) #este campo
    demand_amount= models.CharField(max_length=255, validators=[Validar_Monto_Demandado]) #este campo
    cause_rol = models.CharField(max_length=45, default="C-") 
    
    current_defendant = models.ForeignKey(Defendant, related_name="defendant_lawsuit", on_delete = models.CASCADE)
    current_demand_state = models.ForeignKey(Lawsuit_State, related_name="current_demand_lawsuits", on_delete = models.CASCADE)
    current_court = models.ForeignKey(Court, related_name="current_court_lawsuits", on_delete = models.CASCADE)
    lawsuit_created_by = models.ForeignKey(User, related_name="user_administrate_lawsuit", on_delete = models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LawsuitHistory(models.Model):
    lawsuit_associate = models.ForeignKey(Lawsuit, related_name="lawsuit_history", on_delete = models.CASCADE)
    past_state = models.ForeignKey(Lawsuit_State, related_name="lawsuit_past_state", on_delete = models.CASCADE)
    current_state = models.ForeignKey(Lawsuit_State, related_name="lawsuit_current_state", on_delete = models.CASCADE)
    change_made_by = models.ForeignKey(User, related_name="lawsuit_change", on_delete = models.CASCADE)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

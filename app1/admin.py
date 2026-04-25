from django.contrib import admin
from .models import registration    
from .models import doctor   
from .models import appointment   
from .models import PatientReport
from .models import Manager
from .models import PrescriptionReport
from .models import contactmessage







# Register your models here.
# Patient code 
class registration_(admin.ModelAdmin):
    list_display = ['id','first_name','email','mobile','gender','dob','age','marital_status','bloodgroup','city','pincode','address','photo']
admin.site.register(registration,registration_)


# Admin code 
class doctor_(admin.ModelAdmin):
     list_display = ['id','name','email','phone','department','qualification','experience','availability','gender']
admin.site.register(doctor,doctor_)


class appointment_(admin.ModelAdmin):
     list_display = ['id','doctor','patient','patient_name','patient_email','date','time','consultation_fee','payment_status','created_at']
admin.site.register(appointment,appointment_)


class PatientReport_(admin.ModelAdmin):
     list_display = ['id','patient','doctor','report_title','report_file','description','uploaded_at']
admin.site.register(PatientReport,PatientReport_)


class Manager_(admin.ModelAdmin):
     list_display = ['id','username','email','password']
admin.site.register(Manager,Manager_)


class PrescriptionReport_(admin.ModelAdmin):
     list_display = ['id','doctor','patient','prescription','report_file','created_at']
admin.site.register(PrescriptionReport,PrescriptionReport_)


class contactmessage_(admin.ModelAdmin):
     list_display = ['id','name','email','subject','message']
admin.site.register(contactmessage,contactmessage_)


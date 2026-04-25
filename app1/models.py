from django.db import models
# Create your models here.


# patient code 
class registration(models.Model):

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    mobile = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    age = models.IntegerField()
    marital_status = models.CharField(max_length=15)
    bloodgroup = models.CharField(max_length=5)
    address = models.TextField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=25)
    pincode = models.CharField(max_length=6)
    photo = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.first_name
    
    
# admin code 
class doctor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField()
    fees = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    availability = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name
    
    

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
)
class appointment(models.Model):
    doctor = models.ForeignKey('doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey('registration', on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Paid', 'Paid'),
        ],
        default='Pending'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name}"
    
 
 
class Payment(models.Model):
    appointment = models.OneToOneField('appointment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Success')
    
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Success', 'Success'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    


class PatientReport(models.Model):
    patient = models.ForeignKey('registration', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctor', on_delete=models.CASCADE, null=True, blank=True)
    report_title = models.CharField(max_length=100)
    report_file = models.FileField(upload_to='reports/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.patient.first_name} - {self.report_title}"
    
    
    


class Manager(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    
    

class PrescriptionReport(models.Model):
    doctor = models.ForeignKey('doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey('registration', on_delete=models.CASCADE)

    prescription = models.TextField()
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.first_name} - Prescription"
    




class contactmessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
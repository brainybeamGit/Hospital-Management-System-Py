# Create your views here.
from django.shortcuts import render, redirect , get_object_or_404
from .models import registration,doctor,appointment,Payment,PatientReport,Manager,PrescriptionReport
from django.core.mail import send_mail 
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from datetime import date, timedelta,datetime    
import razorpay
import random
import uuid
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver






# Patient Code 

# REGISTRATION CODE 
def register(request):
    if request.method == 'POST':
        obj = registration()
        obj.first_name = request.POST['first_name']
        obj.middle_name = request.POST['middle_name']
        obj.last_name = request.POST['last_name']
        obj.email = request.POST['email']
        obj.mobile = request.POST['mobile']
        obj.password = request.POST['password']
        obj.gender = request.POST['gender']
        obj.dob = request.POST['dob']
        obj.age = request.POST['age']
        obj.marital_status = request.POST['marital_status']
        obj.bloodgroup = request.POST['bloodgroup']
        obj.city = request.POST['city']
        obj.pincode = request.POST['pincode']
        obj.address = request.POST['add']
        obj.photo = request.FILES['photo']
        already_reg = registration.objects.filter(email = obj.email)
        if already_reg:
            return render(request,'patient/registration.html',{'registered':"already exists"})
        else:
            obj.save()
            send_mail(
                    "Verification mail",                        
                     "this is just an test purpose verification mail", 
                     "prajapativivekk1234@gmail.com",              
                     [obj.email],                                
                     fail_silently=False
                    )
            return redirect('login')
    else:
        return render(request,'patient/registration.html')

# LOGIN CODE 
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = registration.objects.get(email=email)
            if user.password == password:
                otp = random.randint(100000,999999)
                request.session['otp'] = otp
                request.session['email'] = email
                request.session['login'] = user.email
                
                send_mail(
                    'Your Login OTP',
                    f'Your OTP is {otp}',
                    'prjapativivekk1234@gmail.com',
                    [email],
                    fail_silently=False
                )
                return render(request,'patient/otp.html')
            else:
                return render(request,'patient/login.html',{'msg':'Wrong Password'})
        except:
            return render(request,'patient/login.html')
    return render(request,'patient/login.html')


# Verify otp code 
def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST['otp']
        session_otp = request.session.get('otp')
        if str(user_otp) == str(session_otp):
            del request.session['otp']
            return redirect('home')   
        else:
            return render(request,'patient/otp.html',{'msg':'Invalid OTP'})
    return render(request,'patient/otp.html',{'sucess':'Verify sucessfull'})


# Forgot Password - Send OTP
def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = registration.objects.get(email=email)
            otp = random.randint(100000,999999)
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email
            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is {otp}',
                'prajapativivekk1234@gmail.com',
                [email],
                fail_silently=False
            )
            return redirect('verify_reset_otp')
        except:
            return render(request,'patient/forgot_password.html',{'msg':'Email not registered'})
    return render(request,'patient/forgot_password.html')


# Verify OTP
def verify_reset_otp(request):
    if request.method == "POST":
        user_otp = request.POST['otp']
        session_otp = request.session.get('reset_otp')
        if str(user_otp) == str(session_otp):
            return redirect('reset_password')
        else:
            return render(request,'patient/verify_otp.html',{'msg':'Invalid OTP'})
    return render(request,'patient/verify_otp.html')


# Reset Password
def reset_password(request):
    if request.method == "POST":
        new_password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if new_password == confirm_password:
            email = request.session.get('reset_email')
            user = registration.objects.get(email=email)
            user.password = new_password
            user.save()
            del request.session['reset_otp']
            del request.session['reset_email']
            return redirect('login')
        else:
            return render(request,'patient/reset_password.html',{'msg':'Password does not match'})
    return render(request,'patient/reset_password.html')



# Change Password with Email
def change_password(request):
    if request.method == "POST":
        email = request.POST['email']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        try:
            user = registration.objects.get(email=email)
            if user.password == old_password:
                if new_password == confirm_password:
                    user.password = new_password
                    user.save()
                    return render(request,'patient/login.html',
                    {'success':'Password changed successfully'})
                else:
                    return render(request,'patient/change_password.html',
                    {'msg':'New password and confirm password do not match'})
            else:
                return render(request,'patient/change_password.html',
                {'msg':'Old password incorrect'})

        except registration.DoesNotExist:
            return render(request,'patient/change_password.html',
            {'msg':'Email not registered'})

    return render(request,'patient/change_password.html')


# Logout code 
def logout(request):
    del request.session['login']
    return redirect('login')


# Navigation bar code 
def nav(request):
    return render(request,'patient/nav.html')

# Home page code 
def home(request):
    if 'login' in request.session:
        return render(request,'patient/home.html',{'loggin':True})
    else:
        return render(request,'patient/home.html')

# profile code 
def profile(request):
    if 'login' not in request.session:
        return redirect('login')
    email = request.session.get('email')
    if not email:
        return redirect('login')
    user = registration.objects.filter(email=email).first()
    if not user:
        return redirect('login')
    return render(request, 'patient/profile.html', {
        'user': user,
        'loggin': True
    })


# Edit profile code 
def edit_profile(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    user = registration.objects.get(email=email)
    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.middle_name = request.POST.get("middle_name")
        user.last_name = request.POST.get("last_name")
        user.mobile = request.POST.get("mobile")
        user.gender = request.POST.get("gender")
        user.dob = request.POST.get("dob")
        user.bloodgroup = request.POST.get("bloodgroup")
        user.city = request.POST.get("city")
        user.pincode = request.POST.get("pincode")
        user.address = request.POST.get("address")
        if request.FILES.get("photo"):
            user.photo = request.FILES.get("photo")
        user.save()
        return redirect("profile")
    return render(request, "patient/edit_profile.html", {"user": user})

# How many available doctor page 
def patient_doctors(request):
    doctors = doctor.objects.all()

    return render(request, 'patient/doctors.html', {
        'doctors': doctors,
        'loggin': True
    })



# Booking patient Appointment 
def book_appointment(request, id):
    if 'login' not in request.session:
        return redirect('login')
    email = request.session.get('email')
    user = registration.objects.filter(email=email).first()
    if not user:
        return redirect('login')
    doc = get_object_or_404(doctor, id=id)
    if not doc.availability:
        return render(request, 'patient/error.html', {
            'message': 'Doctor is not available'
        })
    today = date.today()
    tomorrow = today + timedelta(days=1)
    if request.method == "POST":
        selected_date = request.POST.get('date')
        selected_time = request.POST.get('time')
        if not selected_date or not selected_time:
            return render(request, 'patient/book_appointment.html', {
                'doctor': doc,
                'error': 'Please select date and time'
            })

        try:
            selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
            selected_time_obj = datetime.strptime(selected_time, "%H:%M").time()
        except ValueError:
            return render(request, 'patient/book_appointment.html', {
                'doctor': doc,
                'error': 'Invalid date or time format'
            })

        if selected_date_obj not in [today, tomorrow]:
            return render(request, 'patient/book_appointment.html', {
                'doctor': doc,
                'error': 'You can only book for today or tomorrow'
            })

        current_time = datetime.now().time()
        if selected_date_obj == today and selected_time_obj <= current_time:
            return render(request, 'patient/book_appointment.html', {
                'doctor': doc,
                'error': 'You cannot book past time slots'
            })

        # Check duplicate slot
        if appointment.objects.filter(
            doctor=doc,
            date=selected_date_obj,
            time=selected_time_obj
        ).exists():
            return render(request, 'patient/book_appointment.html', {
                'doctor': doc,
                'error': 'This time slot is already booked'
            })

        # SAVE APPOINTMENT
        app = appointment.objects.create(
            doctor=doc,
            patient=user,
            patient_name=user.first_name,
            patient_email=user.email,
            date=selected_date_obj,
            time=selected_time_obj,
            consultation_fee=doc.fees,
            payment_status='Pending'
        )

        # CORRECT REDIRECT
        return redirect('payment_page', appointment_id=app.id)

    return render(request, 'patient/book_appointment.html', {
        'doctor': doc,
        'user': user,
        'today': today,
        'tomorrow': tomorrow,
        'loggin': True
    })
    
    


# PAYMENT PAGE
def payment_page(request, appointment_id):
    app = get_object_or_404(appointment, id=appointment_id)

    # Prevent duplicate payment
    if Payment.objects.filter(appointment=app).exists():
        return redirect('payment_success')

    if request.method == "POST":
        method = request.POST.get('payment_method')

        if not method:
            return render(request, 'patient/payment.html', {
                'appointment': app,
                'error': 'Select payment method'
            })

        # CASH PAYMENT
        if method.lower() == "cash":
            Payment.objects.create(
                appointment=app,
                amount=app.consultation_fee,
                payment_method="Cash",
                transaction_id="CASH-" + str(uuid.uuid4())[:8],
                status="Pending"
            )

            app.payment_status = "Pending"
            app.save()

            messages.success(request, "Cash payment selected. Pay at Hospital Counter.")
            return redirect('home')

        # RAZORPAY PAYMENT
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        amount = int(app.consultation_fee * 100)

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })

        request.session['order_id'] = order['id']
        request.session['appointment_id'] = app.id

        return render(request, 'patient/razorpay_payment.html', {
            'order': order,
            'appointment': app,
            'key_id': settings.RAZORPAY_KEY_ID,
            
        })

    return render(request, 'patient/payment.html', {
        'appointment': app,
        'loggin': True
    })


# PAYMENT SUCCESS (VERIFY)
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            params_dict = {
                'razorpay_order_id': request.POST.get('razorpay_order_id'),
                'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
                'razorpay_signature': request.POST.get('razorpay_signature')
            }

            # Verify signature
            client.utility.verify_payment_signature(params_dict)

            app_id = request.session.get('appointment_id')
            app = appointment.objects.get(id=app_id)

            Payment.objects.create(
                appointment=app,
                amount=app.consultation_fee,
                payment_method="Razorpay",
                transaction_id=params_dict['razorpay_payment_id'],
                status="Success"
            )

            app.payment_status = "Paid"
            app.save()

            return render(request, 'patient/payment_success.html')

        except:
            return render(request, 'patient/payment_failed.html')

    return redirect('home')



# MY Appointment page 
def my_appointments(request):
    if 'login' not in request.session:
        return redirect('login')

    email = request.session.get('email')
    user = registration.objects.filter(email=email).first()

    if not user:
        return redirect('login')

    # Fetch all appointments of logged-in user
    appointments = appointment.objects.filter(patient=user).order_by('-date', '-time')

    return render(request, 'patient/my_appointments.html', {
        'appointments': appointments,
        'loggin': True
    })


# Appointment detail page 
def appointment_detail(request, id):
    if 'login' not in request.session:
        return redirect('login')

    app = get_object_or_404(appointment, id=id)

    return render(request, 'patient/appointment_detail.html', {
        'app': app
    })



# Patient report upload page 
def upload_report(request):
    if 'login' not in request.session:
        return redirect('login')
    email = request.session.get('email')
    user = registration.objects.filter(email=email).first()
    if request.method == "POST":
        title = request.POST.get('report_title')
        description = request.POST.get('description')
        file = request.FILES.get('report_file')
        if not title or not file:
            return render(request, 'patient/upload_report.html', {
                'error': 'Title and file are required'
            })
        PatientReport.objects.create(
            patient=user,
            report_title=title,
            report_file=file,
            description=description
        )
        return render(request, 'patient/upload_report.html', {
            'success': 'Report uploaded successfully', 
        'loggin': True
              
        })

    return render(request, 'patient/upload_report.html',{
        'loggin': True
    })


def patient_prescriptions(request, doctor_id):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('patient_login')
    records = PrescriptionReport.objects.filter(
        patient_id=patient_id,
        doctor_id=doctor_id
    ).order_by('-created_at')
    return render(request, 'patient/prescriptions.html', {
        'records': records
    })
    
    

def patient_prescriptions_by_id(request, patient_id, doctor_id):
    patient = get_object_or_404(registration, id=patient_id)
    records = PrescriptionReport.objects.filter(
        patient_id=patient_id,
        doctor_id=doctor_id
    ).order_by('-created_at')
    return render(request, 'patient/prescriptions.html', {
        'records': records,
        'patient': patient,
        'loggin': True
        
    })



# Cancle appointment
def cancel_appointment(request, id):
    if not request.session.get('login'):
        return redirect('login')
    app = get_object_or_404(appointment, id=id)
    if app.patient.email != request.session.get('email'):
        messages.error(request, "Unauthorized action")
        return redirect('my_appointments')
    if app.status == "Pending":
        app.status = "Cancelled"
        app.save()
        messages.success(request, "Appointment cancelled successfully")
    else:
        messages.error(request, "You cannot cancel this appointment")
    return redirect('my_appointments')



from .models import contactmessage

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        contactmessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "Message saved successfully!")

    return render(request, 'patient/contact.html')




# ADMIN PANAL
# Home page of admin 
# REGISTER
def manager_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if Manager.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('manager_register')
        Manager.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        messages.success(request, "Registration successful")
        return redirect('manager_login')
    return render(request, 'manager/register.html')


# LOGIN
def manager_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Manager.objects.get(email=email)
            if check_password(password, user.password):
                #SESSION SET
                request.session['manager_id'] = user.id
                request.session['manager_name'] = user.username
                print("Login Success") 
                return redirect('manager_dashboard')  
            else:
                messages.error(request, "Invalid password")
        except Manager.DoesNotExist:
            messages.error(request, "User not found")
    return render(request, 'manager/login.html')


def view_contacts(request):
    data = contactmessage.objects.all().order_by('-created_at')
    return render(request, 'manager/view_contacts.html', {'data': data})

# DASHBOARD
def manager_dashboard(request):
    if not request.session.get('manager_id'):
        return redirect('manager_login')
    # Calculate total revenue
    revenue_data = Payment.objects.filter(status='Success').aggregate(total=Sum('amount'))
    revenue = revenue_data['total'] if revenue_data['total'] else 0
    context = {
        'revenue': revenue
    }
    return render(request, 'manager/dashboard.html', context)



# LOGOUT
def manager_logout(request):
    request.session.flush()
    return redirect('manager_login')


# Nvigation bar code 
def navbar(request):
    return render(request, 'manager/navbar.html')


# Home page code 
def dashboard(request):
    return render(request, 'manager/dashboard.html')



# ADD Doctors of patient page 
def add_doctor(request):
    error = ""
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        fees = request.POST.get('fees')
        availability = request.POST.get('availability') == 'on'
        # Check if email already exists
        if doctor.objects.filter(email=email).exists():
            error = "Email already used!"
        else:
            #Hash the password here
            hashed_password = make_password(password)
            doctor.objects.create(
                name=name,
                email=email,
                password=hashed_password,   
                gender=gender,
                phone=phone,
                department=department,
                qualification=qualification,
                experience=experience,
                fees = fees,
                availability=availability
            )
            return redirect('add_doctor')
    return render(request, 'manager/add.html', {'error': error})


# Update doctor code 
def update_doctor(request, id):
    doc = get_object_or_404(doctor, id=id)
    error = ""
    success = ""
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        fees = request.POST.get('fees')
        availability = request.POST.get('availability') == 'on'
        # Check email (exclude current doctor)
        if doctor.objects.filter(email=email).exclude(id=id).exists():
            error = "Email already exists!"
        else:
            doc.name = name
            doc.email = email
            doc.gender = gender
            doc.phone = phone
            doc.department = department
            doc.qualification = qualification
            doc.experience = experience
            doc.fees = fees
            doc.availability = availability
            #Update password only if entered
            if password:
                doc.password = make_password(password)
            doc.save()
            success = "Doctor updated successfully!"
    return render(request, 'manager/update.html', {
        'doc': doc,
        'error': error,
        'success': success
    })
    
    
#List Doctors
def doctor_list(request):
    doctors = doctor.objects.all()
    return render(request, 'manager/list.html', {'doctors': doctors})


#Delete Doctor
def delete_doctor(request, id):
    doc = get_object_or_404(doctor, id=id)
    doc.delete()
    return redirect('doctor_list')


# All User Show How many regiter to our clinic
def all_users(request):
    if not request.session.get('manager_id'):
        return redirect('manager_login')

    users = registration.objects.all().order_by('-id')

    return render(request, 'manager/all_users.html', {'users': users})


# Delete User 
def delete_user(request, id):
    if not request.session.get('manager_id'):
        return redirect('manager_login')
    user = registration.objects.get(id=id)
    user.delete()
    return redirect('all_users')


# All User appointment show 
def all_appointments(request):
    if not request.session.get('manager_id'):
        return redirect('manager_login')
    data = appointment.objects.all().order_by('-created_at')
    return render(request, 'manager/all_appointments.html', {'appointments': data})



# Paid or pending appointment change 
@receiver(post_save, sender=Payment)
def update_payment_status(sender, instance, **kwargs):
    appt = instance.appointment
    if instance.status == "Success":
        appt.payment_status = "Paid"
    else:
        appt.payment_status = "Pending"
    appt.save()
    

# Display Payment status
def manager_payments(request):
    payments = Payment.objects.select_related('appointment', 'appointment__doctor', 'appointment__patient')
    return render(request, 'manager/manage_payments.html', {'payments': payments})



def update_payment_status(request, payment_id):
    pay = get_object_or_404(Payment, id=payment_id)
    if request.method == "POST":
        pay.status = request.POST.get('status')
        pay.save()  

    return redirect('manager_payments')










# DOCTOR CODE 
# Login code doctor 
def doctor_login(request):
    error = ""
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            doc = doctor.objects.get(email=email)
            if check_password(password, doc.password):
                request.session['doctor_email'] = doc.email
                request.session['doctor_id'] = doc.id
                request.session['doctor_name'] = doc.name
                return redirect('doctor_dashboard')
            else:
                error = "Invalid Password"
        except doctor.DoesNotExist:
            error = "Invalid Email"
    return render(request, 'doctor/login.html', {'error': error})


# Home page doctor 
def doctor_dashboard(request):
    if 'doctor_email' not in request.session:
        return redirect('doctor_login')
    doc = doctor.objects.get(email=request.session['doctor_email'])
    return render(request, 'doctor/dashboard.html', {'doctor': doc})


# Doctor logout page 
def doctor_logout(request):
    request.session.flush()
    return redirect('doctor_login')

# Doctor navigation bar code 
def doc_navigation(request):
    doctor_name = None

    if 'doctor_email' in request.session:
        try:
            doc = doctor.objects.get(email=request.session['doctor_email'])
            doctor_name = doc.name
        except doctor.DoesNotExist:
            pass
    return render(request, 'doctor/navigation.html', {'doctor_name': doctor_name})



# User appointment show to doctor 
def doctor_appointments(request):
    # Check login
    if 'doctor_id' not in request.session:
        return redirect('doctor_login')
    doctor_id = request.session.get('doctor_id')
    try:
        doc = doctor.objects.get(id=doctor_id)
    except doctor.DoesNotExist:
        return redirect('doctor_login')
    # Fetch ONLY this doctor's appointments
    appointments = appointment.objects.filter(doctor=doc).order_by('-date', '-time')
    context = {
        'doctor': doc,
        'appointments': appointments
    }
    return render(request, 'doctor/appointments.html', context)



# User appointment status change 
def update_appointment_status(request, appointment_id, status):
    if 'doctor_id' not in request.session:
        return redirect('doctor_login')
    doctor_id = request.session.get('doctor_id')
    app = get_object_or_404(appointment, id=appointment_id)
    if app.doctor.id != doctor_id:
        return redirect('doctor_appointments')
    # Update status
    if status in ['Approved', 'Rejected', 'Completed']:
        app.status = status
        app.save()
    return redirect('doctor_appointments')


# Only show current day appointment 
def today_appointments(request):
    today = date.today()
    appointments = appointment.objects.filter(date=today)
    context = {
        'appointments': appointments,
        'today': today
    }
    return render(request, 'doctor/today_appointments.html', context)


# Doctor profile 
def doctor_profile(request):
    doctor_id = request.session.get('doctor_id')  # from login session
    doc = get_object_or_404(doctor, id=doctor_id)
    return render(request, 'doctor/profile.html', {'doctor': doc})


# Diffrent Doctor different patient appointment show 
def doctor_patients_perticular(request):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')
    # fetch all appointments for this doctor
    patients = appointment.objects.filter(doctor_id=doctor_id).order_by('-date')
    return render(request, 'doctor/patients.html', {
        'patients': patients
    })
    
    
# PatientReport Show page 
def view_patient_reports(request, patient_id):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')
    patient = get_object_or_404(registration, id=patient_id)
    # Fetch reports of this patient
    reports = PatientReport.objects.filter(patient=patient).order_by('-uploaded_at')
    return render(request, 'doctor/view_reports.html', {
        'patient': patient,
        'reports': reports
    })
    
    
    
# Doctor send PrescriptionReport to their patient 
def send_prescription(request, patient_id):
    doctor_id = request.session.get('doctor_id')
    if not doctor_id:
        return redirect('doctor_login')
    patient = get_object_or_404(registration, id=patient_id)
    if request.method == "POST":
        prescription = request.POST.get('prescription')
        report_file = request.FILES.get('report_file')
        PrescriptionReport.objects.create(
            doctor_id=doctor_id,
            patient=patient,
            prescription=prescription,
            report_file=report_file
        )
        return redirect('send_prescription', patient_id=patient.id)
    # fetch previous prescriptions
    records = PrescriptionReport.objects.filter(patient=patient).order_by('-created_at')
    return render(request, 'doctor/send_prescription.html', {
        'patient': patient,
        'records': records
    })



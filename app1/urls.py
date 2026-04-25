from django.urls import path
from .views import register,login,verify_otp,home,nav,forgot_password,verify_reset_otp,reset_password,change_password,profile,edit_profile,logout,patient_doctors,book_appointment,payment_page,payment_success,upload_report,my_appointments,appointment_detail,patient_prescriptions,patient_prescriptions_by_id,cancel_appointment,contact
from .views import dashboard,add_doctor,update_doctor,doctor_list,delete_doctor,manager_register,manager_login,manager_dashboard,manager_logout,navbar,all_users,delete_user,all_appointments,update_payment_status,manager_payments,view_contacts
from .views import doctor_login,doctor_dashboard,doctor_logout,doc_navigation,doctor_appointments,update_appointment_status,today_appointments,doctor_profile,doctor_patients_perticular,view_patient_reports,send_prescription



urlpatterns = [
    # paitent urls 
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('verify-otp/',verify_otp,name='verify_otp'),
    path('nav/',nav,name='nav'),
    path('home/',home,name='home'),
    path('profile/',profile, name='profile'),
    path("edit-profile/",edit_profile, name="edit_profile"),
    path('patient_doctors',patient_doctors, name='patient_doctors'),
    # path('book_appointment/<int:id>/',book_appointment, name='book_appointment'),
    path('book_appointment/<int:id>/', book_appointment, name='book_appointment'),
    path('payment_page/<int:appointment_id>/',payment_page, name='payment_page'),
    path('payment_success/',payment_success, name='payment_success'), 
    path('upload_report/', upload_report, name='upload_report'),
    path('my_appointments/', my_appointments, name='my_appointments'),
    path('appointment_detail/<int:id>/',appointment_detail, name='appointment_detail'),
    
    path('patient_prescriptions/',patient_prescriptions, name='patient_prescriptions'),
    path('patient_prescriptions_by_id/<int:patient_id>/<int:doctor_id>/',patient_prescriptions_by_id, name='patient_prescriptions_by_id'),
    path('forgot-password/',forgot_password,name="forgot_password"),
    path('verify-reset-otp/',verify_reset_otp,name="verify_reset_otp"), 
    path('reset-password/',reset_password,name="reset_password"),
    path('change-password/',change_password,name='change_password'),
    path('logout/',logout,name='logout'),
    
    path('cancel_appointment/<int:id>/',cancel_appointment, name='cancel_appointment'),
    path('contact/',contact, name='contact'),
    
   
    
    
    
    
    # ADMIN urls 
    path('manager_register/', manager_register, name='manager_register'),
    path('manager_login/', manager_login, name='manager_login'),
    path('manager_dashboard/',manager_dashboard, name='manager_dashboard'),
    path('manager_logout/', manager_logout, name='manager_logout'),
    path('navbar/', navbar, name='navbar'),
    path('dashboard/',dashboard,name='dashboard'),
    path('add_doctor/',add_doctor, name='add_doctor'),
    path('update_doctor/<int:id>/',update_doctor, name='update_doctor'),
    path('doctor_list/',doctor_list, name='doctor_list'),
    path('delete_doctor/<int:id>/', delete_doctor, name='delete_doctor'),
    path('update_doctor/<int:id>/', update_doctor, name='update_doctor'),
    path('all_users/',all_users, name='all_users'),
    path('delete_user/<int:id>/', delete_user, name='delete_user'),
    path('all_appointments',all_appointments, name='all_appointments'),
   
    path('manager_payments/', manager_payments, name='manager_payments'),
    path('update_payment_status/<int:payment_id>/', update_payment_status, name='update_payment_status'),
    path('view_contacts/',view_contacts, name='view_contacts'),
   
 
    
    # DOCTOR urls 
    path('doctor_login',doctor_login, name='doctor_login'),
    path('doctor_dashboard',doctor_dashboard, name='doctor_dashboard'),
    path('doctor_logout', doctor_logout, name='doctor_logout'),
    path('doc_navigation', doc_navigation, name='doc_navigation'),
     path('doctor_appointments/', doctor_appointments, name='doctor_appointments'),
    path('update_appointment_status/<int:appointment_id>/<str:status>/',update_appointment_status,name='update_appointment_status'),
    path('today_appointments/', today_appointments, name='today_appointments'),
    path('doctor_profile/',doctor_profile, name='doctor_profile'),
    
    path('doctor_patients_perticular', doctor_patients_perticular, name='doctor_patients_perticular'),
    path('view_patient_reports/<int:patient_id>/',view_patient_reports, name='view_patient_reports'),
path('send_prescription/<int:patient_id>/',send_prescription, name='send_prescription'),



]
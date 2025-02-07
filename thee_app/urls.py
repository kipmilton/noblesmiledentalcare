from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'thee_app'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('appointment/', views.appointment, name='appointment'),
    path('accounts/login/', views.login_page, name='login_page'),
    path('accounts/register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('appointment_show/', views.appointment_show, name='appointment_show'),
    path('appointment_delete/<int:id>/', views.appointment_delete, name='appointment_delete'),
    path('appointment_update/<int:appointment_id>', views.appointment_update, name="appointment_update"),
    path('pay', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),
    path('proof/<int:appointment_id>/', views.upload_proof_of_payment, name='upload_proof_of_payment'),
    path('my_appointments/', views.my_appointments, name="my_appointments"),
    path('appointment_mark_done/<int:appointment_id>/mark_done/', views.mark_appointment_done, name='appointment_mark_done'),
]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



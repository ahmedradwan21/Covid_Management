from django.conf import settings
from django.contrib import admin
from django.urls import path
from covid_19 import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('password/reset', views.PasswordResetView.as_view(), name="password_reset"),
    path('password/reset/email_sent', views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password/reset/complete', views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('calculate/', views.calculate_risk, name="calculate_risk"),
    path('success/<int:pk>/', views.success_page, name='success_page'),
    path('update/<int:pk>/', views.update_calculation, name='update_calculation'),
    path('upload/', views.image_upload, name='image_upload'),
    path('display/', views.image_display, name='image_display'),
    path('update_image/<int:image_id>/', views.image_update, name='image_update'),
    path('token' , views.token_send , name="token_send"),
    path('success' , views.success , name='success'),
    path('verify/<auth_token>' , views.verify , name="verify"),
    path('error' , views.error_page , name="error"),
    path('profile1/', views.profile, name='profile1'),
    path('all-users/', views.all_users_view, name='all_users'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='user_profile'),
    path('profile/<int:user_id>/save_report/', views.save_patient_report, name='save_patient_report'),
    path('add_commit/', views.add_commit, name='add_commit'),
    path('view_commits/', views.view_commits, name='view_commits'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('logout/', views.logout_view, name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
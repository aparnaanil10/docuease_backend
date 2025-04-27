from django.contrib import admin
from django.urls import path,include
from users.views import RegisterView, LoginUserView,EditProfileView,ChangePasswordView, HelpView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/register/", RegisterView.as_view(), name="register"),
    path('api/login/', LoginUserView.as_view(), name='login'),
    path('api/edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('api/help/', HelpView.as_view(), name='help'),
    path('api/',include('hospital.urls')),
    path('api/',include('ml_model.urls')),
    path('api/doctors/', include('doctors.urls')),
    path('admin-dashboard/', include('admin_dashboard.urls')),
]

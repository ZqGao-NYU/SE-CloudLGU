from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from accounts.views import register, reset_pwd_code, login, reg_verification, get_profile, modify_pwd, modify_pwd_by_old, update_avatar, update_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register', register, name='register'),
    path('api/login', login, name='login'),
    path('api/sendverification', reg_verification),
    path('api/getprofile', get_profile),
    path('api/forum/', include('forum.urls')),
    path('api/reset', modify_pwd),
    path('api/modifyPwd/old', modify_pwd_by_old),
    path('api/forget', reset_pwd_code, name='forget'),
    path('api/officetime/', include('OfficeHour.urls')),
    path('api/admin/', include('accounts.urls')),
    path('api/updateprofile', update_profile),
    path('api/updatePhoto', update_avatar)


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

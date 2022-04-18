"""Back_End URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from accounts.views import register, ActivateView, authenticationView, Reset_Pwd_Code, login, reg_Verification, getProfile, Modify_Pwd, Modify_Pwd_By_Old, updateAvatar, updateProfile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register', register, name='register'),
    path('api/login', login, name='login'),
    path('api/sendverification', reg_Verification),
    path('api/getprofile', getProfile),
    # path('api/forget',  )
    # path('api/activate/<code>', ActivateView, name='activate'),
    path('api/forum/', include('forum.urls')),
    path('api/reset', Modify_Pwd),
    path('api/modifyPwd/old', Modify_Pwd_By_Old),
    path('api/forget', Reset_Pwd_Code, name='forget'),
    path('api/officetime/', include('OfficeHour.urls')),
    path('api/updateprofile', updateProfile),
    path('api/updatePhoto', updateAvatar)


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

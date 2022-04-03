from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods
from django.views.generic import View, FormView
from django.conf import settings
from .models import User, ConfirmString
from .forms import UserForm
from .utils import send_activation_email
import re
# Create your views here.
# @require_http_methods(["GET"])
def register(request):
    if(request.method == 'GET'):
        form = UserForm()
        context = {'form': form}
        return render(request, 'accounts_create.html', context)
    if(request.method == 'POST'):
        response = {}
        # if not request.is_ajax():
        #     raise Http404("No Ajax Request")
        userID = request.POST.get('userID')
        userName = request.POST.get('userName')
        userEmail = request.POST.get('userEmail')
        password = request.POST.get('password')
        # identify = utils.check_identification(userEmail)
        same_user = User.objects.filter(userEmail = userEmail)
        if same_user:
            response['status'] = "This Email Has Already Been Registered"
            return JsonResponse(response)
        new_user = User()
        new_user.userID = userID
        new_user.userName = userName
        new_user.userEmail = userEmail
        new_user.password = password
        new_user.save()
        # Generate Verification Code
        code = get_random_string(20)
        # Create Confirmation Model
        ConfirmString.objects.create(user=new_user, code=code)
        # Send Confirmation Email
        send_activation_email(request, userEmail, code)
        response['status'] = "You are successfully registered up. To activate the account ,follow the link sent to the mail!"
        return JsonResponse(response)

# @require_http_methods(["POST"])
# def register(request):
#     response = {}

def ActivateView(request, code):
    if(request.method == 'GET'):
        confirm = get_object_or_404(ConfirmString, code=code)
        user = confirm.user
        user.has_confirmed = True
        user.save()

        confirm.delete()

        messages.success(request, "You have successfully activated your account!")
        return redirect('register') # Replace it with login page after integration

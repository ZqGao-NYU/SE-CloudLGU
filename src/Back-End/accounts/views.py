import json
import os
from datetime import datetime

from django.http import Http404, JsonResponse
from django.shortcuts import render, resolve_url
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.conf import settings
from rest_framework.decorators import api_view

from .models import my_user, ConfirmString, Profile
from .forms import UserForm
from .utils import send_activation_email, check_identification, get_verification

def reg_Verification(request):
    if(request.method == 'POST'):
        response = {}
        data = json.loads(request.body)
        userEmail = data['email']
        same_user = my_user.objects.filter(email=userEmail)
        if same_user:
            response['goodMail'] = False
            # response['goodName'] = False
            # response['success'] = False
            # response['message'] = "This Email Has Already Been Used!"
            response['code'] = -1
            return JsonResponse(response)

        # Generate Verification Code
        code = get_verification(settings.VERIFICATION_BITS)
        # new_user = my_user()
        # new_user.email = userEmail
        # new_user.save()
        # Create Confirmation Model
        # ConfirmString.objects.create(user=new_user, code=code)
        # Send Confirmation Email
        send_activation_email("Account Activation", userEmail, code)
        # response['success'] = True
        # response['status'] = "Verification Code Has Already Been Sent to Your Email {Mail}".format(Mail=userEmail)
        response['code'] = code
        response['goodMail'] = True
        return JsonResponse(response)


def Reset_Pwd_Code(request):
    if(request.method == 'POST'):
        response = {}
        userEmail = request.POST.get('userEmail')
        # Check the existance of the user's email
        try:
            user = my_user.objects.get(email=userEmail)
            code = get_verification(settings.VERFICATION_BITS)
            send_activation_email("Password Reset", user.email, code)
            response['code'] = code
            response['success'] = True
            return JsonResponse(response)
        except my_user.DoesNotExist:
            response['success'] = False
            response['code'] = -1
            return JsonResponse(response)

def Modify_Pwd_By_Old(request):
    if(request.method == 'POST'):
        response = {}
        data = json.loads(request.body)
        userEmail = data['userEmail']
        oldPwd = data['oldPassword']
        newPwd = data['newPassword']
        try:
            uLists = my_user.objects.filter(email = userEmail)
            if not uLists.exists():
                response['success'] = False
                return JsonResponse(response)
            user = uLists.get(password=oldPwd)
            user.password=newPwd
            user.save()
            response['success'] = True
            return JsonResponse(response)
        except my_user.DoesNotExist:
            response['success'] = False
            return JsonResponse(response)


def Modify_Pwd(request):
    if(request.method == 'POST'):
        response = {}
        data = json.loads(request.body)
        userEmail = data['userEmail']
        password = data['password'] # User's new password
        try:
            user = my_user.objects.get(email = userEmail)
            user.password = password
            response['success'] = True
            user.save()
            return JsonResponse(response)

        except my_user.DoesNotExist:
            response['success'] = False
            return JsonResponse(response)

def register(request):
    if(request.method == 'GET'):
        form = UserForm()
        context = {'form': form}
        return render(request, 'accounts_create.html', context)
    if(request.method == 'POST'):
        response = {}
        # if not request.is_ajax():
        #     raise Http404("No Ajax Request")
        data = json.loads(request.body)
        userName = data['userName']
        userEmail = data['userEmail']
        password = data['password']
        # code = request.POST.get('code')
        # identify = utils.check_identification(userEmail)
        new_user = my_user()
        new_user.username = userName
        new_user.email = userEmail
        new_user.password = password
        identity = check_identification(new_user.email)
        if identity == 'student':
            new_user.identity = 'student'
        elif identity == 'faculty':
            new_user.identity = 'faculty'
        elif identity == 'invalid':
            # response['goodMail'] = False
            # response['goodName'] = True
            response['success'] = False
            # response['message'] = "Invalid Email Address. You need to use your CUHK(SZ) email to sign up"
            return JsonResponse(response)
        # Administer?
        new_user.has_confirmed = True
        profile = Profile()
        profile.save()
        new_user.profile = profile
        new_user.save()
        response['success'] = True
        return JsonResponse(response)
       # # Confirmation (Check Verification Code):
       #  try:
       #      confirm = ConfirmString.objects.get(code=code)
       #  except:
       #      context = {}
       #      context['success'] = False
       #      context['message'] = 'Verification Code Not Match'
       #      return JsonResponse(context) #  Replace it with login page or successful inform page after integration
       #  c_time = confirm.c_time
       #  now = datetime.now()
       #  if now > c_time + datetime.timedelta(settings.CONFIRM_TIME):
       #      context = {}
       #      confirm.delete()
       #      context['success'] = False
       #      context['message'] = 'Verfication Code Expired, Please Resend The Code!'
       #      return JsonResponse(context)
       #  else:
       #      user = confirm.user
       #      user.has_confirmed = True
       #      user.save()
       #      confirm.delete()
       #      response['success'] = True
       #      response['message'] = 'You have successfully registered up! Thank you for your support!'
       #      return JsonResponse(response)

        # # Generate Verification Code
        # code = get_verification(settings.VERFICATION_BITS)
        #
        # # Create Confirmation Model
        # ConfirmString.objects.create(user=new_user, code=code)
        # # Send Confirmation Email
        # send_activation_email(request, userEmail, code)

# @require_http_methods(["POST"])
# def register(request):
#     response = {}

def ActivateView(request, code):
    print("Check")
    if(request.method == 'GET'):
        try:
            confirm = ConfirmString.objects.get(code=code)
            user = confirm.user
            user.has_confirmed = True
            user.save()
            confirm.delete()
        except:
            context = {}
            context['message'] = 'Invalid Authentication Request. This link may already been used!'
            context['uri'] = reverse('register')
            return render(request, 'verification_fail.html', context) #  Replace it with login page or successful inform page after integration



        messages.success(request, "You have successfully activated your account!")
        return redirect('register') # Replace it with login page or successful inform page after integration



def authenticationView(request):
    return render(request,'auth.html',locals())


def login(request):
    response = {}
    if request.session.get('is_login', None):  # 不允许重复登录
        response['success'] = False
        response['info'] = "Repeat Logins are not allowed！"
        return JsonResponse(response)
    if request.method == 'POST':
        data = json.loads(request.body)
        userEmail = data['userEmail']
        password = data['password']

        try:
            user = my_user.objects.get(email=userEmail)
            if user.password == password:
                request.session['is_login'] = True
                request.session['userID'] = user.id
                request.session['userEmail'] = user.email
                response['success'] = True
                # response['token'] = {"info":"Login Success", "identity":user.identity, "userID":user.id}
                response['token'] = user.id
                return JsonResponse(response)

            else:#返回json
                response['success'] = False
                response['info'] = "Incompatible Password"
                return JsonResponse(response)
        except my_user.DoesNotExist:
            response['success'] = False
            # response['info'] = "This Account Does not Exist！Please Try Again"
            response['token'] = -1
            return JsonResponse(response)

    # login_form = UserForm()
    # return render(request, 'login/login.html', locals())


def updateProfile(request):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        # userEmail = request.session['userEmail']#session不知道可不可以这么用，不行的话让前端传id
        uID = data['token']
        user = my_user.objects.get(id=uID)

        user.Profile.userIntro = data['userIntro']
        user.username = data['userName']

        # Save Photo
        photo = request.FILES.get('userPhoto')
        user.Profile.userPhoto = photo
        user.save()
        return JsonResponse({'success':True})


def getProfile(request):
    if(request.method == 'POST'):
        response = {}
        data = json.loads(request.body)
        uID = data['token']
        user = my_user.objects.get(id=uID)
        response['userPhoto'] = "http://" + request.get_host()  + user.profile.userPhoto.url
        response['userIntro'] = user.profile.userIntro
        response['userName'] = user.username
        response['userEmail'] = user.email
        response['userIdentity'] = user.identity
        return JsonResponse(response)



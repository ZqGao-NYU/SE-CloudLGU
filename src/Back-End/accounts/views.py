import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.db.models import F
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

from .models import my_user, ConfirmString, Profile
from .forms import UserForm
from .utils import send_activation_email, check_identification, get_verification, send_Inform


def reg_verification(request):
    if request.method == 'POST':
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


def reset_pwd_code(request):
    if request.method == 'POST':
        response = {}
        data = json.loads(request.body)
        userEmail = data['userEmail']
        # Check the existance of the user's email
        try:
            user = my_user.objects.get(email=userEmail)
            code = get_verification(settings.VERIFICATION_BITS)
            send_activation_email("Password Reset", user.email, code)
            response['code'] = code
            response['success'] = True
            return JsonResponse(response)
        except my_user.DoesNotExist:
            response['success'] = False
            response['code'] = -1
            return JsonResponse(response)


def modify_pwd_by_old(request):
    if request.method == 'POST':
        response = {}
        data = json.loads(request.body)
        userEmail = data['userEmail']
        oldPwd = data['oldPassword']
        newPwd = data['newPassword']
        try:
            uLists = my_user.objects.filter(email=userEmail)
            if not uLists.exists():
                response['success'] = False
                return JsonResponse(response)
            user = uLists.get(password=oldPwd)
            user.password = newPwd
            user.save()
            response['success'] = True
            return JsonResponse(response)
        except my_user.DoesNotExist:
            response['success'] = False
            return JsonResponse(response)


def modify_pwd(request):
    if request.method == 'POST':
        response = {}
        data = json.loads(request.body)
        userEmail = data['userEmail']
        password = data['password']  # User's new password
        try:
            user = my_user.objects.get(email=userEmail)
            user.password = password
            response['success'] = True
            user.save()
            return JsonResponse(response)

        except my_user.DoesNotExist:
            response['success'] = False
            return JsonResponse(response)


def register(request):
    if request.method == 'GET':
        form = UserForm()
        context = {'form': form}
        return render(request, 'accounts_create.html', context)
    if request.method == 'POST':
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
        new_user.save()
        profile.user = new_user
        profile.save()
        response['success'] = True
        return JsonResponse(response)


def activate_view(request, code):
    print("Check")
    if request.method == 'GET':
        try:
            confirm = ConfirmString.objects.get(code=code)
            user = confirm.user
            user.has_confirmed = True
            user.save()
            confirm.delete()
        except:
            context = {'message': 'Invalid Authentication Request. This link may already been used!',
                       'uri': reverse('register')}
            return render(request, 'verification_fail.html',
                          context)  # Replace it with login page or successful inform page after integration

        messages.success(request, "You have successfully activated your account!")
        return redirect('register')  # Replace it with login page or successful inform page after integration


def authentication_view(request):
    return render(request, 'auth.html', locals())


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

            else:  # 返回json
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


def update_profile(request):
    if request.method == 'POST':
        # try:
        data = json.loads(request.body)
        # userEmail = request.session['userEmail']#session不知道可不可以这么用，不行的话让前端传id
        uID = data['userID']
        user = my_user.objects.get(id=uID)

        user.profile.userIntro = data['userIntro']
        user.username = data['userName']

        user.profile.save()
        user.save()
        return JsonResponse({'success': True})
        # except:
        #     return JsonResponse({'success':False})
    else:
        return JsonResponse({'success': False})


def update_avatar(request):
    if request.method == 'POST':
        # data = json.loads(request.body)
        # photo = data['photo']
        # uID = data['userID']
        photo = request.FILES.get('photo')
        uID = request.POST.get('userID')
        user = my_user.objects.get(id=uID)
        # Save Photo
        user.profile.userPhoto = photo
        user.profile.save()
        user.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def get_profile(request):
    if (request.method == 'POST'):
        response = {}
        data = json.loads(request.body)
        uID = data['token']
        user = my_user.objects.get(id=uID)
        response['userPhoto'] = "http://" + request.get_host() + user.profile.userPhoto.url
        response['userIntro'] = user.profile.userIntro
        response['userName'] = user.username
        response['userEmail'] = user.email
        response['userIdentity'] = user.identity
        return JsonResponse(response)


def get_user_list(request):
    response = {}
    userList = my_user.objects.annotate(userName=F('username'), userEmail=F('email'),
                                        userPassword=F('password'), userIntro=F('profile__userIntro'),
                                        userIdentity=F('identity')).values('userName', 'userEmail',
                                                                           'userPassword', 'userIdentity', 'userIntro')
    serialized_q = json.dumps(list(userList), cls=DjangoJSONEncoder)
    response['lists'] = json.loads(serialized_q)
    # json_list = serializers.serialize("json", userList)
    # response['lists'] = json_list

    return JsonResponse(response)


def reset_profile(request):
    data = json.loads(request.body)
    userEmail = data['userEmail']

    userName = data['userName']
    userIntro = data['userIntro']
    password = data['userPassword']
    userIdentity = data['userIdentity']
    user = my_user.objects.get(email=userEmail)
    user.username = userName
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = Profile(user=user)
    profile.userIntro = userIntro
    profile.save()
    user.identity = userIdentity
    user.password = password
    user.save()

    response = {'success': True}
    return JsonResponse(response)


def delete_user(request):
    data = json.loads(request.body)
    userEmail = data['userEmail']
    user = my_user.objects.get(email=userEmail)
    user.delete()
    send_Inform(userEmail)
    response = {'success': True}
    return JsonResponse(response)

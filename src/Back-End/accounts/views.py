import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import F
from django.conf import settings
from django.views.decorators.http import require_POST

from .models import MyUser, Profile
from .forms import UserForm
from .utils import send_activation_email, check_identification, get_verification, send_inform


@require_POST
def reg_verification(request):
    """Generate the verification code email for the user to register a new account."""
    response = {}
    data = json.loads(request.body)
    userEmail = data['email']
    same_user = MyUser.objects.filter(email=userEmail)
    if same_user:
        response['goodMail'] = False
        response['code'] = -1
        return JsonResponse(response)

    # Generate Verification Code
    code = get_verification(settings.VERIFICATION_BITS)
    # Send Confirmation Email
    send_activation_email("Account Activation", userEmail, code)
    response['code'] = code
    response['goodMail'] = True
    return JsonResponse(response)


@require_POST
def reset_pwd_code(request):
    """Generate the verification code email for the user to modify their password."""
    response = {}
    data = json.loads(request.body)
    userEmail = data['userEmail']
    try:
        user = MyUser.objects.get(email=userEmail)  # Check the existence of the user's email
        code = get_verification(settings.VERIFICATION_BITS)
        send_activation_email("Password Reset", user.email, code)
        response['code'] = code
        response['success'] = True
        return JsonResponse(response)
    except MyUser.DoesNotExist:
        response['success'] = False
        response['code'] = -1
        return JsonResponse(response)


@require_POST
def modify_pwd_by_old(request):
    """Modify the password with the old password"""
    response = {}
    data = json.loads(request.body)
    userEmail = data['userEmail']
    oldPwd = data['oldPassword']
    newPwd = data['newPassword']
    try:
        uLists = MyUser.objects.filter(email=userEmail)  # Get the user's email first
        if not uLists.exists():
            response['success'] = False
            return JsonResponse(response)
        user = uLists.get(password=oldPwd)
        user.password = newPwd
        user.save()
        response['success'] = True
        return JsonResponse(response)
    except MyUser.DoesNotExist:  # If the user doesn't exist
        response['success'] = False
        return JsonResponse(response)


@require_POST
def modify_pwd(request):
    """Modify the password through verification code sent with email"""
    response = {}
    data = json.loads(request.body)
    userEmail = data['userEmail']
    password = data['password']  # User's new password
    try:
        user = MyUser.objects.get(email=userEmail)
        user.password = password
        response['success'] = True
        user.save()
        return JsonResponse(response)

    except MyUser.DoesNotExist:
        response['success'] = False
        return JsonResponse(response)


@require_POST
def register(request):
    """Register a new account

    Key Arguments:
    userName -- User's name that can be seen by other users
    userEmail -- User's email to register the account
    password -- User's password for the account
    """
    response = {}
    data = json.loads(request.body)
    userName = data['userName']
    userEmail = data['userEmail']
    password = data['password']
    # Generate a new user object
    new_user = MyUser()
    new_user.username = userName
    new_user.email = userEmail
    new_user.password = password
    identity = check_identification(new_user.email)  # Use email address to verify the identity of the users.
    if identity == 'student':
        new_user.identity = 'student'
    elif identity == 'faculty':
        new_user.identity = 'faculty'
    elif identity == 'invalid':
        response['success'] = False
        return JsonResponse(response)
    new_user.has_confirmed = True
    profile = Profile()
    new_user.save()
    profile.user = new_user
    profile.save()
    response['success'] = True
    return JsonResponse(response)


@require_POST
def login(request):
    """Login with user's email and password"""
    response = {}
    if request.session.get('is_login', None):  # No repeated login
        response['success'] = False
        response['info'] = "Repeat Logins are not allowed！"
        return JsonResponse(response)
    if request.method == 'POST':
        data = json.loads(request.body)
        userEmail = data['userEmail']
        password = data['password']

        try:
            user = MyUser.objects.get(email=userEmail)
            if user.password == password:
                request.session['is_login'] = True
                request.session['userID'] = user.id
                request.session['userEmail'] = user.email
                response['success'] = True
                response['token'] = user.id
                return JsonResponse(response)

            else:
                response['success'] = False
                response['info'] = "Incompatible Password"
                return JsonResponse(response)
        except MyUser.DoesNotExist:
            response['success'] = False
            response['token'] = -1
            return JsonResponse(response)


@require_POST
def update_profile(request):
    """Update user's profile

    Key Arguments:
    userIntro -- User's self-introduction
    userName -- User's nickname shown to other users
"""
    if request.method == 'POST':
        data = json.loads(request.body)
        uID = data['userID']
        user = MyUser.objects.get(id=uID)

        user.profile.userIntro = data['userIntro']
        user.username = data['userName']

        user.profile.save()
        user.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@require_POST
def update_avatar(request):
    """Update user's avatar"""
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        uID = request.POST.get('userID')
        user = MyUser.objects.get(id=uID)
        # Save Avatar to the location set in the models.
        user.profile.userPhoto = photo
        user.profile.save()
        user.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@require_POST
def get_profile(request):
    """Get a certain user's profile through their user's ID"""
    response = {}
    data = json.loads(request.body)
    uID = data['token']
    user = MyUser.objects.get(id=uID)
    response['userPhoto'] = "http://" + request.get_host() + user.profile.userPhoto.url  # Use http to locate the avatar
    response['userIntro'] = user.profile.userIntro
    response['userName'] = user.username
    response['userEmail'] = user.email
    response['userIdentity'] = user.identity
    return JsonResponse(response)


@require_POST
def get_user_list(request):
    """Get the list of users. This function only belongs to Administer"""
    response = {}
    userList = MyUser.objects.annotate(userName=F('username'), userEmail=F('email'),
                                       userPassword=F('password'), userIntro=F('profile__userIntro'),
                                       userIdentity=F('identity')).values('userName', 'userEmail',
                                                                          'userPassword', 'userIdentity', 'userIntro')
    serialized_q = json.dumps(list(userList), cls=DjangoJSONEncoder)
    response['lists'] = json.loads(serialized_q)

    return JsonResponse(response)


@require_POST
def reset_profile(request):
    """Reset the profile or password of a certain user. This function only belongs to Administer"""
    data = json.loads(request.body)
    userEmail = data['userEmail']
    userName = data['userName']
    userIntro = data['userIntro']
    password = data['userPassword']
    userIdentity = data['userIdentity']
    user = MyUser.objects.get(email=userEmail)
    user.username = userName
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = Profile(user=user)
    profile.userIntro = userIntro
    profile.save()  # Save the updated records
    user.identity = userIdentity
    user.password = password
    user.save()

    response = {'success': True}
    return JsonResponse(response)


@require_POST
def delete_user(request):
    """Delete the user and send an inform"""
    data = json.loads(request.body)
    userEmail = data['userEmail']
    user = MyUser.objects.get(email=userEmail)
    user.delete()
    send_inform(userEmail)  # Send inform to the email address that will be deleted
    response = {'success': True}
    return JsonResponse(response)

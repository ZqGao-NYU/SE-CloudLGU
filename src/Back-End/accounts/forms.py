from django import forms

class UserForm(forms.Form):
    userID= forms.CharField(label = 'userid', max_length=64, widget=forms.TextInput(attrs={'class':'form-control'}))
    userName = forms.CharField(label = 'userName', max_length=64, widget=forms.TextInput(attrs={'class':'form-control'}))
    userEmail = forms.CharField(label = 'Email Address', widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label = 'password', max_length=128, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label = 'password_confirm', max_length=128, widget=forms.PasswordInput(attrs={'class':'form-control'}))


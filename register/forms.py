from django import forms
from register.models import Team
from register.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', required=True)
    team = forms.ModelChoiceField(queryset=Team.objects.all())

    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
            'team',
            'password1',
            'password2',
        }

        labels = {
            'first_name': 'Name',
            'last_name': 'Last Name',
            'team': 'Team',
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        team = self.cleaned_data['team']

        if commit:
            user.save()
            user_profile = UserProfile.objects.create(
                user=user, team=Team.objects.get(name=team))
            user_profile.save()

        return user

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Retype Password'
        self.fields['team'].widget.attrs['class'] = 'form-control'


class TeamRegistrationForm(forms.Form):
    social_name = forms.CharField(max_length=80)
    name = forms.CharField(max_length=80)
    email = forms.EmailField()
    city = forms.CharField(max_length=50)
    found_date = forms.DateField()

    class Meta:
        model = Team

    def save(self, commit=True):
        team = Team()
        team.social_name = self.cleaned_data['social_name']
        team.name = self.cleaned_data['name']
        team.email = self.cleaned_data['email']
        team.city = self.cleaned_data['city']
        team.found_date = self.cleaned_data['found_date']

        if commit:
            team.save()

    def __init__(self, *args, **kwargs):
        super(TeamRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['social_name'].widget.attrs['class'] = 'form-control'
        self.fields['social_name'].widget.attrs['placeholder'] = 'Social Name'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['found_date'].widget.attrs['class'] = 'form-control'
        self.fields['found_date'].widget.attrs['placeholder'] = 'Found date'


class ProfilePictureForm(forms.Form):
    img = forms.ImageField()

    class Meta:
        model = UserProfile
        fields = ['img']

    def save(self, request, commit=True):
        user = request.user.userprofile_set.first()
        user.img = self.cleaned_data['img']

        if commit:
            user.save()

        return user

    def __init__(self, *args, **kwargs):
        super(ProfilePictureForm, self).__init__(*args, **kwargs)
        self.fields['img'].widget.attrs['class'] = 'custom-file-input'
        self.fields['img'].widget.attrs['id'] = 'validatedCustomFile'

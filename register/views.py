from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from projects.models import Task
from .models import UserProfile
from .models import Invite
from .forms import RegistrationForm
from .forms import TeamRegistrationForm
from .forms import ProfilePictureForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            created = True
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            context = {'created': created}
            return render(request, 'register/reg_form.html', context)
        else:
            return render(request, 'register/reg_form.html', context)
    else:
        form = RegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'register/reg_form.html', context)


@login_required
def usersView(request):
    users = UserProfile.objects.all()
    tasks = Task.objects.all()
    context = {
        'users': users,
        'tasks': tasks,
    }
    return render(request, 'register/users.html', context)


@login_required
def user_view(request, profile_id):
    user = UserProfile.objects.get(id=profile_id)
    context = {
        'user_view': user,
    }
    return render(request, 'register/user.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        img_form = ProfilePictureForm(request.POST, request.FILES)
        print('PRINT 1: ', img_form)
        context = {'img_form': img_form}
        if img_form.is_valid():
            img_form.save(request)
            updated = True
            context = {'img_form': img_form, 'updated': updated}
            return render(request, 'register/profile.html', context)
        else:
            return render(request, 'register/profile.html', context)
    else:
        img_form = ProfilePictureForm()
        context = {'img_form': img_form}
        return render(request, 'register/profile.html', context)


@login_required
def newTeam(request):
    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = TeamRegistrationForm()
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'register/new_team.html', context)
        else:
            return render(request, 'register/new_team.html', context)
    else:
        form = TeamRegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'register/new_team.html', context)


@login_required
def invites(request):
    return render(request, 'register/invites.html')


@login_required
def invite(request, profile_id):
    profile_to_invite = UserProfile.objects.get(id=profile_id)
    logged_profile = get_active_profile(request)
    if not profile_to_invite in logged_profile.friends.all():
        logged_profile.invite(profile_to_invite)
    return redirect('core:index')


@login_required
def deleteInvite(request, invite_id):
    logged_user = get_active_profile(request)
    logged_user.received_invites.get(id=invite_id).delete()
    return render(request, 'register/invites.html')


@login_required
def acceptInvite(request, invite_id):
    invite = Invite.objects.get(id=invite_id)
    invite.accept()
    return redirect('register:invites')


@login_required
def remove_friend(request, profile_id):
    user = get_active_profile(request)
    user.remove_friend(profile_id)
    return redirect('register:friends')


@login_required
def get_active_profile(request):
    user_id = request.user.userprofile_set.values_list()[0][0]
    return UserProfile.objects.get(id=user_id)


@login_required
def friends(request):
    if request.user.is_authenticated:
        user = get_active_profile(request)
        friends = user.friends.all()
        context = {
            'friends': friends,
        }
    else:
        users_prof = UserProfile.objects.all()
        context = {
            'users_prof': users_prof,
        }
    return render(request, 'register/friends.html', context)

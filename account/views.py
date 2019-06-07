from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
# from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# from .forms import LoginForm
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact


## Custom Made login() method
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated Successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'account/login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                'new_user': new_user
            }
            return render(request, 'account/register_done.html', context)
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'account/register.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated Successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context ={
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'account/edit_profile.html', context)


@login_required
def HomeView(request):
    context = {
        'section':'homeview'
    }
    return render(request, 'index.html', context)



@login_required
def user_list(request):
    users = User.objects.filter(is_active=True).exclude(username='admin')
    return render(request, 'account/user/list.html', {'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    # print(user.followers.all)
    return render(request, 'account/user/detail.html', {'user': user})


def ajax_required():
    pass

from django.views.decorators.http import require_POST
from .decorators import ajax_required

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    print(user_id, action)
    if user_id and action:
        print("true")
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                print("person to follow: ", user)
                print("person to follow's profile: ", user.profile)
                print("request for user: ", request.user)
                print("request for profile: ", request.user.profile)
                Contact.objects.get_or_create(user_from=request.user.profile,
                                              user_to=user.profile)
                # create_action(request.user, 'is following', user.profile)
            else:
                Contact.objects.filter(user_from=request.user.profile,
                                       user_to=user.profile).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})
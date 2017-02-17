from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

# Imports the Post class
from samemoment.models import *


# Action for the default /samemoment/ route.
@login_required
def home(request):
    # Gets a list of all the posts in the todo-list database.
    all_posts = Post.objects.all().order_by('-create_time')

    return render(request, 'samemoment/index.html', {'posts': all_posts})


# Action for the /samemoment/create-post route.
@login_required
def add_post(request):
    errors = []
    if 'post' not in request.POST or not request.POST['post']:
        errors.append('You must enter a post to add.')
    else:
        new_post = Post(text=request.POST['post'],
                        user=request.user,
                        ip_addr=request.META['REMOTE_ADDR'])
        new_post.save()

    # Sets up data needed to generate the view, and generates the view
    posts = Post.objects.all().order_by('-create_time')
    context = {'posts': posts, 'errors': errors}
    return render(request, 'samemoment/index.html', context)

# Action for the /samemoment/view-profile route
@login_required
def view_profile(request, post_user):
    errors = []
    user = User.objects.get(username = post_user)

    posts = Post.objects.filter(user=user).order_by('-create_time')
    context = {'posts': posts, 'errors': errors, 'view_user': user}
    return render(request, 'samemoment/profile.html', context)

# Action for the /samemoment/delete-post route.
@login_required
def delete_post(request, post_id):
    errors = []

    if request.method != 'POST':
        errors.append('Deletes must be done using the POST method')
    else:
        # Deletes the post if present in the post database.
        try:
            post_to_delete = Post.objects.get(id=post_id)
            post_to_delete.delete()
        except ObjectDoesNotExist:
            errors.append('The post did not exist in our database.')

    posts = Post.objects.all().order_by('-create_time')
    context = {'posts': posts, 'errors': errors}
    return render(request, 'samemoment/index.html', context)

@transaction.atomic
def register(request):
    context = {}
    errors = []
    context['errors'] = errors

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'samemoment/register.html', context)

    # Check the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']

    if not 'first_name' in request.POST or not request.POST['first_name']:
        errors.append('first_name is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['first_name'] = request.POST['first_name']
    if not 'last_name' in request.POST or not request.POST['last_name']:
        errors.append('last_name is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['last_name'] = request.POST['last_name']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')

    if errors:
        # Required fields are missing.  Display errors, now.
        return render(request, 'samemoment/register.html', context)

    if request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if User.objects.select_for_update().filter(username = request.POST['username']).exists():
        errors.append('Username is already taken.')

    if errors:
        # Required fields are missing.  Display errors, now.
        return render(request, 'samemoment/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password1'],
                                        first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'])
    new_user.save()

    # Logs in the new user and redirects to the index.html
    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password1'])

    login(request, new_user)
    return redirect('/samemoment/')

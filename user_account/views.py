from django.contrib import messages
from django.http import JsonResponse
from .models import CustomUser, Review,Thread
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from communities.models import CommunityCategory, CommunityPost
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from user_account.models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Notification
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.db.models import Avg,Count
from .models import *
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
import logging
from django.shortcuts import render
from .models import Notification
from django.shortcuts import render
from .models import Notification
from django.shortcuts import render
from .models import Notification
from django.shortcuts import render
from .models import Notification

# def notification_view(request):
#     notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'user-account-dashboard/account-notification.html', {'notifications': notifications})

# from django.shortcuts import render
# from user_account.models import Notification

# def notifications_view(request):
#     user = request.user
#     notifications = Notification.objects.filter(user=user)
#     print(f'Notifications: {list(notifications)}')  # Print notifications to console
#     return render(request, 'user-account-dashboard/account-notification.html', {'notifications': notifications})

from django.shortcuts import render
from .models import Notification

def accountNotification(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user-account-dashboard/account-notification.html', {'notifications': notifications})



logger = logging.getLogger(__name__)

def send_notification(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        message = request.POST.get('message')
        
        try:
            user = User.objects.get(username=username)
            Notification.objects.create(user=user, message=message)
            logger.debug(f'Notification sent to {username} with message: {message}')
            return JsonResponse({'status': 'success'}, status=200)
        except User.DoesNotExist:
            logger.error(f'User with username {username} not found.')
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



User = get_user_model()


# def get_notifications(request):
#     if request.is_ajax() and request.method == 'GET':
#         notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
#         notification_list = list(notifications.values('message', 'created_at'))
#         for notification in notification_list:
#             notification['created_at'] = notification['created_at'].strftime('%b %d, %Y %H:%M')  # Format date
#         return JsonResponse({'notifications': notification_list})
#     return JsonResponse({'notifications': []})



# @csrf_exempt
# def set_chat_user(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_id = data.get('user_id')
#             user_name = data.get('user_name')
#             user_email = data.get('user_email')

#             if not user_id or not user_name or not user_email:
#                 return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)

#             request.session['chat_user_id'] = user_id
#             request.session['chat_user_name'] = user_name
#             request.session['chat_user_email'] = user_email
#             return JsonResponse({'status': 'success'})
#         except json.JSONDecodeError:
#             return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# @login_required
# def chat_messages(request):
#     user_id = request.GET.get('user_id')
#     if not user_id:
#         return JsonResponse({'status': 'error', 'message': 'User ID not provided'}, status=400)
#     try:
#         messages = Message.objects.filter(room__participants__id=user_id).values('username', 'message', 'timestamp')
#         return JsonResponse({'messages': list(messages)})
#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# @login_required
# def chat_view(request, user_id):
#     user = get_object_or_404(CustomUser, id=user_id)
#     room_name = f"chat_{request.user.id}_{user_id}"
#     return render(request, 'user-account-dashboard/chat.html', {'user': user, 'room_name': room_name })

@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    all_users = CustomUser.objects.exclude(id=request.user.id)
     # Add all users to a thread
    for user in all_users:
        # Check if a thread already exists between the current user and another user
        thread, created = Thread.objects.get_or_create(first_person=request.user, second_person=user)

        # If no thread is found with the current user as the second person
        if not created:
            thread, created = Thread.objects.get_or_create(first_person=user, second_person=request.user)
            
    context = {
        'Threads': threads,
        'Users': all_users,
    }
    return render(request, 'user-account-dashboard/chat.html', context)
    # return render(request,'realchat.html')

def chat_view(request, username):
    other_user = get_object_or_404(CustomUser, username=username)
    # thread = Thread.objects.get_or_create_thread(request.user, other_user)
    return render(request, 'user-account-dashboard/chat.html', {'other_user': other_user})

# def chat(request):
#     # Your view logic here, if any
#     return render(request, 'user-account-dashboard/chat.html')

# def rooms(request):
#     rooms=Room.objects.all()
#     return render(request,'user-account-dashboard/chat.html',{"rooms":rooms})

# def room(request,slug):
#     room_name=Room.objects.get(slug=slug).name
#     messages=Message.objects.filter(room=Room.objects.get(slug=slug))
#     context={"slug":slug,"room_name":room_name,"messages":messages}
#     return render(request,"user-account-dashboard/chat.html",context)

@login_required
def message(request):
    return render(request, 'messages.html')

@login_required
def search_profiles(request):
    query = request.GET.get('q')
    results = CustomUser.objects.filter(
        Q(full_name__icontains=query) |
        Q(role__icontains=query) |
        Q(company__icontains=query) |
        Q(city__icontains=query) |
        Q(zip_code__icontains=query)
    )
    return render(request, 'user-account-dashboard/messages.html', {'results': results, 'query': query})

# Create your views here.
def signUp(request):
    if request.method == "POST":
        email = request.POST.get('gmail_id')
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not email or not password or not confirm_password or not full_name:
            messages.error(request, "All fields are required.")
            return render(request, 'sign-up.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'sign-up.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'sign-up.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already taken.")
            return render(request, 'sign-up.html')

        user = CustomUser(
            email=email,
            full_name=full_name,
            username=username,
            password=make_password(password)
        )
        user.save()

        return redirect('signUpSteps', user_id=user.id)

    return render(request, 'sign-up.html')

def signUpSteps(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect('signUp')

    if request.method == "POST":
        role = request.POST.get('role')
        sector = request.POST.get('sector')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        skills_expertise = request.POST.get('skills_expertise')
        cv=request.POST.get('cv')

        # Validate that all fields are provided
        if not all([role, sector, city, zip_code, skills_expertise]):
            messages.error(request, "All fields are required.")
            return render(request, 'sign-up-steps.html', {'user': user})

        # Update the user with additional information
        user.role = role
        user.sector = sector
        user.city = city
        user.zip_code = zip_code
        user.skills_expertise = skills_expertise
        user.cv=cv
        user.save()

        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect('viewProfile', username=user.username)
    
    context = {
        'user': user,
        
    }

    return render(request, 'sign-up-steps.html', context)

def signIn(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'sign-in.html')

        try:
            user_exists = CustomUser.objects.get(username=username)
            print(f"User exists: {user_exists}")
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return render(request, 'sign-in.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in.")
            return redirect('viewProfile', username=user.username)
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'sign-in.html')

    return render(request, 'sign-in.html')
@login_required
def updateProfile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    if request.method == 'POST':
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        
            # Update profile information
            user.full_name = request.POST.get('full_name', user.full_name)
            user.username = request.POST.get('username', user.username)
            user.email = request.POST.get('email', user.email)
            user.phone = request.POST.get('phone', user.phone)
            user.nationality = request.POST.get('nationality', user.nationality)
            user.gender = request.POST.get('gender', user.gender)
            user.role = request.POST.get('role', user.role)
            user.sector = request.POST.get('sector', user.sector)
            user.skills_expertise = request.POST.get('skills_expertise', user.skills_expertise)
            user.address = request.POST.get('address', user.address)

            #saving profile
            user.save()
            messages.success(request, "Profile updated successfully!")

            return redirect('viewProfile',username=user.username) 
    
        # Handle email update
        new_email = request.POST.get('email')
        if new_email and new_email != user.email:
            user.email = new_email
            #saving profile
            user.save()
            messages.success(request, "Email updated successfully!")

            return redirect('viewProfile',username=user.username) 

        # Handle password change
        current_pass = request.POST.get('current_pass')
        new_password = request.POST.get('new_password')
        cf_new_password = request.POST.get('cf_new_password')
        
        if current_pass and new_password and cf_new_password:
            if new_password == cf_new_password:
                if authenticate(username=user.username, password=current_pass):
                    user.set_password(new_password)
                    user.save()
                    print("Password updated successfully.")
                    messages.success(request, "Password updated successfully.")
                    login(request, user)
                    return redirect('viewProfile', user.username)
                else:
                    print("Current password is incorrect.")
                    messages.error(request, "Current password is incorrect.")
                    return redirect('viewProfile', user.username)
            else:
                print("New passwords do not match.")
                messages.error(request, "New passwords do not match.")
                return redirect('viewProfile', user.username)

    return render(request, 'user-account-dashboard/user-profile.html', {'user': user})



@login_required(login_url='signin')
def logOut(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def userProfile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    context = {
        'user': user,
    }
    return render(request, 'user-account-dashboard/account-detail.html', context)

@login_required(login_url='signin')

@login_required(login_url='signin')
def accountProjects(request):
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        title = request.POST.get('title')
        sector = request.POST.get('sector')
        sub_sector = request.POST.get('sub_sector')
        description = request.POST.get('description')
        pdf_file=request.FILES.get('pdf')
       
        user = request.user
        try:
            category = CommunityCategory.objects.get(id=category_id)
            data = CommunityPost(
                user=user,
                category=category,
                title=title,
                sector=sector,
                sub_sector=sub_sector,
                description=description,
                pdf=pdf_file,
            )
            data.save()
            messages.success(request, 'Successfully added new Project!')
        except CommunityCategory.DoesNotExist:
            messages.error(request, 'Please select the Role field to proceed!')

        return redirect('account_projects')

    communities = CommunityCategory.objects.all()
    projects = CommunityPost.objects.filter(user=request.user)

    context = {
        'communities': communities,
        'projects': projects,
    }
    return render(request, 'user-account-dashboard/account-projects.html', context)

@login_required(login_url='signin')
def accountProject_update(request, id=None):
    post = get_object_or_404(CommunityPost, id=id)
    
    if request.method == 'POST':
        post.category_id = request.POST.get('category')
        post.sector = request.POST.get('sector')
        post.sub_sector = request.POST.get('sub_sector')
        post.title = request.POST.get('title')
        post.description = request.POST.get('description')
        post.pdf=request.FILES.get('pdf')
        
        post.save()
        messages.success(request, "Post updated successfully.")
        return redirect('account_projects')
    
    elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'category': post.category_id,
            'title': post.title,
            'sector':post.sector,
            'sub_sector':post.sub_sector,
            'description':post.description,
            'pdf':post.pdf.url if post.pdf else None,
        }
        return JsonResponse(data)
    
    context = {
        'post': post,
    }
    
    return render(request, 'user-account-dashboard/account-projects.html', context)

@login_required(login_url='signin')
def ProjectDelete(request, id = None):
    delete_project = CommunityPost.objects.get(id = id)
    delete_project.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('account_projects')

def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts= CommunityPost.objects.filter(user=user)
    reviews = Review.objects.filter(reviewed_user=user)

    paginator = Paginator(posts, 3)
    page_num = request.GET.get('page')
    posts_data = paginator.get_page(page_num)
    
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Calculate distribution of ratings
    rating_counts = reviews.values('rating').annotate(count=Count('rating')).order_by('rating')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        content = request.POST.get('content')
        reviewer = request.user
        Review.objects.create(reviewer=reviewer, reviewed_user=user, rating=rating, content=content)
        return redirect('profile', username=username)

    context = {
        'user_data': user,
        'posts': posts,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'rating_counts': rating_counts,
        'posts_data':posts_data,
    }
    return render(request, 'user-account-dashboard/user-profile.html', context)

@login_required(login_url='signin')
def Messages(request):
    return render(request, 'user-account-dashboard/messages.html')

@login_required(login_url='signin')
def chat(request):
    return render(request, 'user-account-dashboard/chat.html')

def PasswordReset(request):
    if request.method == "POST":
        email = request.POST.get('email')
        associated_users = CustomUser.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "password/password_reset_email.txt"
                c = {
                    "email": user.email,
                    "domain": request.META['HTTP_HOST'],
                    "site_name": "Website",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }
                email = render_to_string(email_template_name, c)
                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            return redirect('password_reset_done')
    return render(request, "password/password_reset.html")

def PasswordResetConfirm(request, uidb64=None, token=None):
    if request.method == 'POST':
        uid = force_str(urlsafe_base64_decode(uidb64))
        user =CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('password1')
            if new_password and new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return redirect('password_reset_complete')
            else:
                return HttpResponse("Passwords do not match.")
        else:
            return HttpResponse("Invalid token.")
    return render(request, 'password/password_reset_confirm.html', {'uidb64': uidb64, 'token': token})

def PasswordResetDone(request):
    return render (request,'password/password_reset_done.html')
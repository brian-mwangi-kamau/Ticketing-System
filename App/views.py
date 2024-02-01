import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db import connections
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import CustomUser, Ticket, StaffInfo, Comment
from .forms import UserSignupForm, StaffSignupForm, LoginForm, TicketForm, CommentForm, StatusForm, UserProfileForm, StaffProfileForm, StaffInfoForm



#pylint: disable=no-member
     
# Regular user signup view
def user_signupview(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = CustomUser(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
            )
            user.set_password(form.cleaned_data['password1'])
            user = form.save(commit=False)
            user.save() 
    else:
        form = UserSignupForm()
    return render(request, 'registration/user_signup.html', {'form': form})


# Query database for staff IDs for verification of staff - used when signing up staff users
def get_staff_info(staff_id):
    with connections['default'].cursor() as cursor:
        cursor.execute(
            "SELECT staff_username FROM staff_info WHERE staff_id = %s", [staff_id]
        )
        row = cursor.fetchone()
        if row:
            return row[0]
        return None
    

# Staff user signup view
def staff_signupview(request):
    if request.method == 'POST':
        form = StaffSignupForm(request.POST)
        if form.is_valid():
            # Validate that the user is a member of staff using their staff ID
            staff_id = form.cleaned_data['staff_id']
            staff_username = get_staff_info(staff_id)
            
            if staff_username == form.cleaned_data['username']:
                user = form.save(commit=False)
                user.is_staff = True # Save the user as staff
                user.save()

                login(request, user)
                return redirect(reverse('dashboard'))
    else:
        form = StaffSignupForm()
    return render(request, 'registration/staff_signup.html', {'form': form})
    

# Log in - all users
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect(reverse('dashboard'))
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user
    if user.is_staff and not user.is_admin:
        username = request.user.username
        tickets = Ticket.objects.filter(Q(assigned_to=user)).order_by('-created_at')
        total_tickets = Ticket.objects.filter(Q(assigned_to=user)).distinct().count()
        open_tickets = Ticket.objects.filter(Q(assigned_to=user), status='open').count()
        resolved_tickets = Ticket.objects.filter(Q(assigned_to=user), status='closed').count()
        
        context = {
            'user': user,
            'username': username,
            'tickets': tickets,
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'resolved_tickets': resolved_tickets,
        }
        return render(request, 'dashboard/staff_dashboard.html', context)

    elif user.is_admin:
        total_tickets = Ticket.objects.all().count()
        open_tickets = Ticket.objects.filter(status='open').count()
        resolved_tickets = Ticket.objects.filter(status='closed').count()
        staff_users = CustomUser.objects.filter(is_staff=True)
        
        staff_data = []

        for staff in staff_users:
            assigned_tickets = Ticket.objects.filter(assigned_to=staff).count()
            open_tickets_staff = Ticket.objects.filter(Q(assigned_to=staff, status='open')).count()
            resolved_tickets_staff = Ticket.objects.filter(Q(assigned_to=staff, status='closed')).count()

            staff_data.append({
                'id': staff.id,
                'first_name': staff.first_name,
                'assigned_tickets': assigned_tickets,
                'open_tickets_staff': open_tickets_staff,
                'resolved_tickets_staff': resolved_tickets_staff,
            })

        
            context = {
                'staff_users': staff_users,
                'total_tickets': total_tickets,
                'assigned_tickets': assigned_tickets,
                'open_tickets': open_tickets,
                'resolved_tickets': resolved_tickets,
                'open_tickets_staff': open_tickets_staff,
                'resolved_tickets_staff': resolved_tickets_staff,
            }
        
        return render(request, 'dashboard/admin_dashboard.html', context)
    
    else:
        username = request.user.username
        profile_picture = request.user.profile_picture
        tickets = Ticket.objects.filter(Q(creator=user)).order_by('-created_at')
        total_tickets = Ticket.objects.filter(Q(creator=user)).distinct().count()
        open_tickets = Ticket.objects.filter(Q(creator=user), status='open').count()
        resolved_tickets = Ticket.objects.filter(Q(creator=user), status='closed').count()
        
        context = {
            'user': user,
            'username': username,
            'profile_picture': profile_picture,
            'tickets': tickets,
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'resolved_tickets': resolved_tickets,
        }
        return render(request, 'dashboard/user_dashboard.html', context)
    

@login_required
def profile(request):
    user = request.user
    
    if user.is_staff and not user.is_admin:
        if request.method == 'POST':
            form = StaffProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                user.save()
                return redirect(reverse('profile'))
        else:
            form = StaffProfileForm(initial={
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'profile_picture': user.profile_picture,
            })
        return render(request, 'profile/staff_profile.html', {'user': user, 'form': form})
    
    elif user.is_staff == False and user.is_admin == False:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                user.save()
                return redirect(reverse('profile'))
        else:
            form = UserProfileForm(initial={
                'profile_picture': user.profile_picture,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number
            })
        return render(request, 'profile/user_profile.html', {'form': form})
    
    else:
        pass
    
    
    
# Query database for staff departments for ticket assigning purposes.
def get_staff_dept(ticket_category):
    try:
        staff_details = StaffInfo.objects.get(department=ticket_category)
        return staff_details.department
    except StaffInfo.DoesNotExist:
        return None

           
# The creation of new tickets
def create_ticket(request):
    user = request.user
    if user.is_staff == False and user.is_admin == False:
        if request.method == 'POST':
            form = TicketForm(request.POST, request.FILES)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.creator = request.user
                ticket_category = form.cleaned_data['category']
                staff_dept = get_staff_dept(ticket_category)  # Get the staff department based on the ticket category

                if staff_dept:
                    staff_member = StaffInfo.objects.filter(department=staff_dept).first()
                    if staff_member:
                        ticket.assigned_to = staff_member.user  # Assign the ticket to the staff user associated with the department
                    
                ticket.save()
                return redirect(reverse('dashboard'))
        else:
            form = TicketForm()
        return render(request, 'tickets/new_ticket.html', {'form': form})
    else:
        return HttpResponse("You can't create a ticket!")


@login_required
def get_ticket_details(request, id):
    user = request.user
    try:
        ticket = Ticket.objects.get(pk=id)
    except Ticket.DoesNotExist:
        return HttpResponse("Ticket not found!")

    comments = Comment.objects.filter(Q(ticket=ticket)).order_by('created_at')
    
    if ticket.creator == user or ticket.assigned_to == user:
        context = {
            'user': user,
            'ticket': ticket,
            'comments': comments,
        }        

        if ticket.status == 'open':  # Comments can only be added to open tickets.
            if request.method == 'POST':
                comment_form = CommentForm(request.POST)

                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.message = comment_form.cleaned_data['message']
                    comment.image = comment_form.cleaned_data['image']
                    comment.creator = user
                    comment.ticket = ticket
                    comment.save()
                    messages.success(request, "Comment added successfully!")
                    return redirect('ticket-details', id=id)
            else:
                comment_form = CommentForm()
                context['comment_form'] = comment_form
        else:
            context['comment_form'] = None  # No comment form for closed tickets
            context['message'] = "This ticket is closed!"      
    else:
        return HttpResponse("You do not have permission to access this ticket!")
    
    if ticket.assigned_to == user:
        if request.method == 'POST':
            status_form = StatusForm(request.POST, instance=ticket)
            if status_form.is_valid():
                status_form.save()
                return redirect('ticket-details', id=id)
        else:
            status_form = StatusForm(instance=ticket, initial={'status': ticket.status})
            context['status_form'] = status_form

    return render(request, 'tickets/ticket_details.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
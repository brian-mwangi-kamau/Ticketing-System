from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("You must provide an email!")
        if not email:
            raise ValueError("You must provide a username!")

        user = self.model(
            email=self.normalize_email(email),
            username = username,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username = username,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=15, unique=True)
    
    first_name = models.CharField(max_length=10, null=True, blank=True)
    last_name = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    profile_picture  = models.ImageField(upload_to='media/', null=True, blank=True)

    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(auto_now_add=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now_add=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.username}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class StaffInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='staff_user')
    DEPT_CATEGORY_CHOICES = (
        ('Functionality Issues', 'Functionality Issues'),
        ('Assistance with Software Installations', 'Assistance with Software Installations'),
        ('Slow Application Response', 'Slow Application Response'),
        ('Hardware Upgrades', 'Hardware Upgrades'),
        ('Hardware Inspections', 'Hardware Inspections'),
    )
    department = models.CharField(max_length=100, choices=DEPT_CATEGORY_CHOICES)
    staff_id = models.CharField(max_length=10, unique=True, null=True, blank=False)
    
    def __str__(self):
        return f"{self.user.first_name} - {self.staff_id}" 
    

class Ticket(models.Model):
    id =  models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False)
    message = models.TextField(blank=False)
    image = models.ImageField(upload_to='media/', blank=True)
    TICKET_PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    priority = models.CharField(max_length=10, choices=TICKET_PRIORITY_CHOICES, blank=False, default='medium')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tickets')
    TICKET_CATEGORY_CHOICES = (
        ('Functionality Issues', 'Functionality Issues'),
        ('Assistance with Software Installations', 'Assistance with Software Installations'),
        ('Slow Application Response', 'Slow Application Response'),
        ('Hardware Upgrades', 'Hardware Upgrades'),
        ('Hardware Inspections', 'Hardware Inspections'),
    )
    category = models.CharField(max_length=50, choices=TICKET_CATEGORY_CHOICES, default='slow_application_response')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_tickets')
    TICKET_STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    status = models.CharField(max_length=10, choices=TICKET_STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.status}"
    

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='created_comments')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.message}"
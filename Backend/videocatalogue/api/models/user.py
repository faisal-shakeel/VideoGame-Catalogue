from re import L

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

def get_profile_image_path(self, _):
    return f'profile_images/users/{self.pk}/{str(uuid.uuid4())}.png'


def get_default_profile_image_path():
    return f'profile_images/{"default_profile_image.png"}'

class UserManager(BaseUserManager):
    def create_user(self,username, email, first_name, last_name, password):
        if not username:
            raise ValueError('User must have a username')
        if not first_name:
            raise ValueError('User must have a first name')
        if not last_name:
            raise ValueError('User must have a last name')
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self,username, email, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name= last_name,
            password= password
        )
        user.is_staff = True
        user.save(using = self._db)
        return user

gender_choices = [('male', 'male'), ('female', 'female'), ('others', 'others')]
class User(AbstractBaseUser):
    username                = models.CharField(max_length=30, unique=True)
    email                   = models.EmailField(max_length=60, blank=True, null=True)
    first_name              = models.CharField(max_length=30)
    last_name               = models.CharField(max_length=30)
    full_name               = models.CharField(max_length=90, blank=True, null=True)
    profile_image           = models.ImageField(max_length=255, upload_to=get_profile_image_path, null=True, blank=True, default=get_default_profile_image_path)
    is_delete               = models.BooleanField(default=False)
    roles                   = models.ManyToManyField('Role', related_name='users')
    is_staff                = models.BooleanField(default=False)
    gender                  = models.CharField(max_length=10, choices=gender_choices, default=gender_choices[0][0])
    created_at              = models.DateTimeField(auto_now_add=True)
    created_by              = models.ForeignKey('self', related_name='+', blank=True, null=True, on_delete=models.CASCADE)
    updated_at              = models.DateTimeField(auto_now=True)
    updated_by              = models.ForeignKey('self', related_name='+', blank=True, null=True, on_delete=models.CASCADE)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    def delete(self):
        self.is_delete = True
        self.save()
        
    def has_permission(self, perm):
        perm_li = []
        for role in self.roles.all():
            role_permissions = role.permissions.all()
            for permission in role_permissions:
                perm_li.append(permission.code_name)
        if perm in perm_li:
            return True
        else:
            return False
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self,*args,**kwargs):
        self.full_name = self.first_name + " " + self.last_name
        return super().save(*args,**kwargs)

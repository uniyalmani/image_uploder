from django.db import models


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManger(BaseUserManager):
    def create_user(self, email, name, password=None, confirm_password=None):
        """
        create and save user of given email, name, password
        """ 
        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(email=self.normalize_email(email),
                          name=name,
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        
        
        user = self.model(email=email,
                          name=name,
                          )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    
    # password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    objects = UserManger()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    @property
    def is_authenticated(self):
        return True if self.id else False

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return  self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


    



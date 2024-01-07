from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    # Custom user model manager with email as the unique identifier
    def create_user(self, first_name, last_name, email, password, **extra_fields):

        # Create superuser with the given email and password.
        if not email:
            raise ValueError("The email must be set")
        if not password:
            raise ValueError("The password must be set")
        email = self.normalize_email(email)
        first_name = first_name.capitalize()
        last_name = last_name.capitalize()
        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, first_name, last_name, email, password, **extra_fields):

        # Create superuser with the given email and password.
        extra_fields.setdefault('role', 1)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('role') != 1:
            raise ValueError('Superuser must have role of Global Admin')
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")
        
        return self.create_user(first_name, last_name, email, password, **extra_fields)
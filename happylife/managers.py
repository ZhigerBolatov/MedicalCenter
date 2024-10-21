from django.contrib.auth.base_user import BaseUserManager


class HappyLifeUserManager(BaseUserManager):
    def create_user(self, IIN, password, **extra_fields):
        if IIN is None:
            raise ValueError('IIN is Required')
        if password is None:
            raise ValueError('Password is Required')
        user = self.model(IIN = IIN, **extra_fields)
        user.set_password(password)  # Set password with hash SHA256
        user.save()
        return user

    def create_superuser(self, IIN, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(IIN, password, **extra_fields)


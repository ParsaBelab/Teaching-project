from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, username, password):
        if not phone_number:
            raise ValueError('کاربر باید شماره تلفن داشته باشد')
        if not username:
            raise ValueError('کاربر باید نام کاربری داشته باشد')

        user = self.model(phone_number=phone_number, username=username)
        user.set_password(password)
        user.is_active = True
        user.save(using=self.db)
        return user

    def create_superuser(self, phone_number, username, password):
        user = self.create_user(phone_number, username, password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self.db)
        return user

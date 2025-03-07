import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CodeHub.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")

    if User.objects.filter(username=username).exists():
        print("Superuser with this username already exists.")
    else:
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superuser created successfully!")

if __name__ == "__main__":
    create_superuser()

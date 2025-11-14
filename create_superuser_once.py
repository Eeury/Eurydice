import os
from django.contrib.auth import get_user_model

def main():
    User = get_user_model()

    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

    if not username or not email or not password:
        print("Superuser env vars missing. Skipping.")
        return

    if User.objects.filter(username=username).exists():
        print("Superuser already exists. Skipping creation.")
        return

    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"Superuser '{username}' created successfully.")

if __name__ == "__main__":
    main()

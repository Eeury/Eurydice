import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Eurydice.settings')
django.setup()

from django.contrib.auth import get_user_model

def main():
    User = get_user_model()

    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    email = os.getenv("DJANGO_SUPERUSER_EMAIL")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

    if not username or not email or not password:
        print("ERROR: Superuser env vars missing. Skipping.")
        print("Required: DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD")
        return

    print(f"Attempting to create/update superuser: {username}")
    
    # Check if user exists
    user = User.objects.filter(username=username).first()
    
    if user:
        print(f"User '{username}' already exists. Updating password and ensuring superuser status...")
        user.set_password(password)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        print(f"Superuser '{username}' updated successfully!")
    else:
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"Superuser '{username}' created successfully!")
        except Exception as e:
            print(f"Error creating superuser: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    # Verify the user can authenticate
    user = User.objects.get(username=username)
    if user.check_password(password):
        print(f"✓ Password verification successful for '{username}'")
    else:
        print(f"✗ WARNING: Password verification failed for '{username}'")
    
    print(f"Email: {email}")
    print(f"Is superuser: {user.is_superuser}")
    print(f"Is staff: {user.is_staff}")
    print(f"Is active: {user.is_active}")

if __name__ == "__main__":
    main()

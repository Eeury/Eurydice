#!/usr/bin/env python
"""
Verify superuser credentials by attempting to authenticate.
"""
import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Eurydice.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate

def main():
    User = get_user_model()
    
    username = os.getenv("DJANGO_SUPERUSER_USERNAME")
    password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
    
    if not username or not password:
        print("ERROR: DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD must be set")
        return
    
    print(f"Verifying credentials for user: {username}")
    
    # Check if user exists
    try:
        user = User.objects.get(username=username)
        print(f"✓ User '{username}' exists")
        print(f"  - Email: {user.email}")
        print(f"  - Is superuser: {user.is_superuser}")
        print(f"  - Is staff: {user.is_staff}")
        print(f"  - Is active: {user.is_active}")
    except User.DoesNotExist:
        print(f"✗ User '{username}' does not exist")
        return
    
    # Try to authenticate
    authenticated_user = authenticate(username=username, password=password)
    if authenticated_user:
        print(f"✓ Authentication successful!")
        print(f"  - Can login: Yes")
    else:
        print(f"✗ Authentication failed!")
        print(f"  - Password is incorrect or user is inactive")
        print(f"\nTo reset password, run:")
        print(f"  python create_superuser_once.py")

if __name__ == "__main__":
    main()


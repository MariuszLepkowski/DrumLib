import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DrumLib.settings")
django.setup()

from django.contrib.auth import get_user_model
from user_management_app.models import Profile  # Adjust the path if necessary

User = get_user_model()

# Superuser credentials from environment variables
USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME')
EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL')
PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

# Ensure all required environment variables are set
if not USERNAME or not EMAIL or not PASSWORD:
    print("❌ Missing environment variables for superuser creation. Skipping.")
    exit(1)

# Check if superuser exists
user, created = User.objects.get_or_create(
    username=USERNAME,
    defaults={"email": EMAIL, "is_superuser": True, "is_staff": True}
)

if created:
    user.set_password(PASSWORD)
    user.save()
    print(f"✅ Superuser '{USERNAME}' has been created.")
else:
    print(f"ℹ️ Superuser '{USERNAME}' already exists.")

    # Ensure the password is set correctly (avoid login issues)
    if not user.check_password(PASSWORD):
        user.set_password(PASSWORD)
        user.save()
        print(f"🔄 Password for '{USERNAME}' has been updated.")

# Ensure profile exists for the superuser
profile, profile_created = Profile.objects.get_or_create(user=user)

if profile_created:
    print(f"✅ Profile for '{USERNAME}' has been created.")
else:
    print(f"ℹ️ Profile for '{USERNAME}' already exists.")

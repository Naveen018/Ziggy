from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User, UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print("User Profile created")
    else:  # When user info is updated(created flag will be false and this block will be executed)
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:  # This scenario is when user if created but user profile is deleted somehow and if we try to update user info it throws error since profile is deleted
            # Create user profile if it doesn't exist
            UserProfile.objects.create(user=instance)
        print("User is updated")


# Once user is created we need to created user profile(So user is created by User model and it becomes sender, it should send a msg that
# user object is created to receiver which created user profile)

# post_save(post_save_create_profile_receiver, sender=User)

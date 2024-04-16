from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Distributor, Vroom_User

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        email = instance.email.lower() 
        # Check if the email domain is associated with a distributor
        if email.endswith('.vroom@gmail.com'):
            Distributor.objects.create(
                first_name=instance.first_name,
                last_name=instance.last_name,
                contact=instance.contact,
                email=email,
                image=instance.image
            )
        else:
            Vroom_User.objects.create(
                first_name=instance.first_name,
                last_name=instance.last_name,
                contact=instance.contact,
                email=email,
                image=instance.image
            )
    else:
        # If the user profile already exists, update it
        email = instance.email.lower()  # Normalize email address
        try:
            distributor_profile = Distributor.objects.get(email=email)
            distributor_profile.first_name = instance.first_name
            distributor_profile.last_name = instance.last_name
            distributor_profile.contact = instance.contact
            distributor_profile.image = instance.image
            distributor_profile.save()
        except Distributor.DoesNotExist:
            try:
                vroom_user_profile = Vroom_User.objects.get(email=email)
                vroom_user_profile.first_name = instance.first_name
                vroom_user_profile.last_name = instance.last_name
                vroom_user_profile.contact = instance.contact
                vroom_user_profile.image = instance.image
                vroom_user_profile.save()
            except Vroom_User.DoesNotExist:
                # If neither distributor nor vroom user profile exists, do nothing
                pass

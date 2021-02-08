from .models import User, Employment
from django.db.models.signals import post_save
from django.dispatch import receiver
import clearbit
from decouple import config


@receiver(post_save, sender=User)
def create_employment(sender, instance, created, **kwargs):
    if created:
        user = instance

        clearbit.key = config("CLEARBIT_SECRET_KEY")

        response = clearbit.Enrichment.find(email=user.email, stream=True)

        if response is None or response["company"] is None:
            Employment.objects.create(
                user=instance,
                company_name="Unkown",
                company_location="Unkown",
                title="Unkown",
                seniority="Unkown",
            )
        else:
            Employment.objects.create(
                user=instance,
                company_name=response["company"]["name"],
                company_location=response["company"]["location"],
                title=response["person"]["employment"]["title"],
                seniority=response["company"]["name"],
            )


@receiver(post_save, sender=User)
def save_employment(sender, instance, **kwargs):
    instance.employment.save()
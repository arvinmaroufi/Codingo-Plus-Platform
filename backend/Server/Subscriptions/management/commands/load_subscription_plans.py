import json
from django.core.management.base import BaseCommand
from Subscriptions.models import SubscriptionPlan
from Server.settings import BASE_DIR
import os



class Command(BaseCommand):
    help = 'Load subscription plans from a JSON file into the database'

    def handle(self, *args, **kwargs):
        # Correcting the file path by removing square brackets
        with open(os.path.join(BASE_DIR, 'static/json/subscription_plans.json'), encoding='utf-8') as file:
            data = json.load(file)

        # Loop through plans
        for plan_data in data:
            plan, created = SubscriptionPlan.objects.get_or_create(
                name=plan_data['name'],
                slug=plan_data['slug'],
                level=plan_data['level'],
                description=plan_data['description'],
                price_per_day=plan_data['price_per_day']
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded subscription plans!'))
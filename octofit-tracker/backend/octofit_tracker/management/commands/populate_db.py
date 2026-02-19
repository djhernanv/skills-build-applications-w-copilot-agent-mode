from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# Import models from octofit_tracker.models to avoid conflicts
from octofit_tracker.models import Team, Activity, Leaderboard, Workout

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data in the correct order to avoid unhashable errors
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()


        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (superheroes)
        users = [
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'team': marvel},
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': dc},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'team': dc},
        ]
        user_objs = {}
        for u in users:
            user = User.objects.create_user(username=u['username'], email=u['email'], password='password')
            user_objs[u['username']] = user

        # Create activities
        Activity.objects.create(user=user_objs['spiderman'], activity_type='Running', duration=30, team=marvel)
        Activity.objects.create(user=user_objs['ironman'], activity_type='Cycling', duration=45, team=marvel)
        Activity.objects.create(user=user_objs['batman'], activity_type='Swimming', duration=25, team=dc)
        Activity.objects.create(user=user_objs['wonderwoman'], activity_type='Yoga', duration=60, team=dc)

        # Create leaderboard
        Leaderboard.objects.create(team=marvel, points=75)
        Leaderboard.objects.create(team=dc, points=85)

        # Create workouts
        Workout.objects.create(name='Hero HIIT', description='High intensity interval training for heroes.', suggested_for='Marvel')
        Workout.objects.create(name='Power Yoga', description='Strength and flexibility for champions.', suggested_for='DC')

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FootprintRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='footprint_records')
    date = models.DateField(default=timezone.now)
    total_footprint = models.FloatField(help_text="Total carbon footprint in kg CO2e")
    transportation_footprint = models.FloatField(default=0)
    food_footprint = models.FloatField(default=0)
    home_energy_footprint = models.FloatField(default=0)
    consumption_footprint = models.FloatField(default=0)
    
    # Store the detailed analysis from Gemma
    detailed_analysis = models.TextField(blank=True)
    
    # Store the raw user responses for reference
    raw_responses = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username}'s footprint on {self.date} - {self.total_footprint} kg CO2e"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    region = models.CharField(max_length=100, blank=True)
    household_size = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def get_average_footprint(self):
        records = self.user.footprint_records.all()
        if not records:
            return 0
        return sum(record.total_footprint for record in records) / records.count()

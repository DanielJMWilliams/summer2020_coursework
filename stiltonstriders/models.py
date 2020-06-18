from django.db import models

# Create your models here.
class Event(models.Model):
    EVENT_TYPES = (
        ("Race", "Race"),
        ("Training Session", "Training Session"),
    )
    name = models.CharField(max_length=64)
    description = models.TextField()
    event_type = models.CharField(max_length=64, choices=EVENT_TYPES)
    dateTime = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.dateTime}"
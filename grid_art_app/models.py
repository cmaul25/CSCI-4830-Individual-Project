from django.db import models
from django.contrib.auth.models import User

class Pixel(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    color = models.CharField(max_length=7)  # stores hex color e.g. #FF5733
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('x', 'y')  # ensures no duplicate pixels

    def __str__(self):
        return f"Pixel({self.x}, {self.y}) - {self.color}"
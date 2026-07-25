from django.db import models 

class AccessLog(models.Model):
    ip =    models.GenericIPAddressField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.country} - {self.state} - {self.city}"
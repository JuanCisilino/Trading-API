from django.db import models

class Trade(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('executed', 'Executed'),
        ('error', 'Error'),
    ]

    RESULT_CHOICES = [
        ('win', 'Win'),
        ('loss', 'Loss'),
        ('error', 'Error'),
    ]

    asset = models.CharField(max_length=20)
    direction = models.CharField(max_length=10)
    amount = models.FloatField()
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, null=True, blank=True)
    profit = models.FloatField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=10, default="PRACTICE")

    def __str__(self):
        return f"{self.asset} - {self.direction} - {self.result}"

class Strategy(models.Model):
    asset = models.CharField(max_length=20)
    amount = models.FloatField()
    timeframe = models.IntegerField(default=60)
    mode = models.CharField(max_length=10, default="PRACTICE")
    active = models.BooleanField(default=True)
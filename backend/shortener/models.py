from django.db import models

# Create your models here.
import string
import random
from django.db import models

class URL(models.Model):
    long_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        length = 6
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(chars, k=length))
            if not URL.objects.filter(short_code=code).exists():
                return code
            
    def __str__(self):
        return f"{self.short_code} -> {self.long_url}"
import random
import string
from django.db import models

class URL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=6, unique=True, blank=True)

    def generate_short_code(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(6))

    def save(self, *args, **kwargs):
        # Generate a short code if it's not provided
        if not self.short_code:
            while True:
                short_code = self.generate_short_code()
                if not URL.objects.filter(short_code=short_code).exists():
                    self.short_code = short_code
                    break
        super().save(*args, **kwargs)

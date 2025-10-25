from django.db import models

# Create your models here.


class Domain(models.Model):
    name = models.CharField(max_length=255)
    sip_url = models.URLField()

    def __str__(self):
        return self.name


class Extension(models.Model):
    number = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.number


class Customer(models.Model):
    email = models.EmailField(unique=True)
    extension = models.OneToOneField(Extension, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Auto-generate display name from email if not provided
        if not self.display_name:
            self.display_name = self.email.split('@')[0].capitalize()
        super().save(*args, **kwargs)

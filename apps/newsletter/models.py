from django.db import models

# Create your models here.
class Newsletter(models.Model):
    email = models.EmailField(null=True)
    title = models.TextField(null=True)
    message = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ("Newsletter")
        verbose_name_plural = ("Newsletters")
        ordering = ["-created"]

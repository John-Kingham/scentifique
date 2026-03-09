from django.db import models


class About(models.Model):
    """
    Content for the About page.
    """

    title = models.CharField(max_length=200, unique=True)
    content = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated"]
        verbose_name_plural = "About"

    def __str__(self):
        return self.title

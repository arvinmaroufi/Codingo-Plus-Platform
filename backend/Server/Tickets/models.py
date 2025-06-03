from django.db import models


class Department(models.Model):
    """Represents a department where tickets can be categorized."""
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دپارتمان")  # Department name, must be unique
    description = models.TextField(blank=True, verbose_name="توضیحات")  # Optional description of the department

    def __str__(self):
        """Returns a human-readable representation of the department."""
        return self.name

    class Meta:
        """Meta options for the Department model."""
        verbose_name = "دپارتمان"
        verbose_name_plural = "دپارتمان ‌ها"
        


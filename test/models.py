from django.db import models

class Vulnerability(models.Model):
    cve_id = models.CharField(max_length=20, unique=True)
    published_date = models.DateTimeField()
    last_modified_date = models.DateTimeField()
    severity = models.CharField(max_length=20)
    fixed = models.BooleanField(default=False)

    def __str__(self):
        return self.cve_id

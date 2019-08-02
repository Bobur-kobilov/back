from django.db import models


# Create your models here.
class MtsVersion(models.Model):
    id              = models.BigAutoField(primary_key=True)
    version         = models.CharField(max_length=20, blank=False, null=False)
    device          = models.CharField(max_length=50, blank=False, null=False, unique=True)
    
    class Meta:
        db_table = "mts_version"
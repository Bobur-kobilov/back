from django.db import models
from account.models import User
# Create your models here.
class ManagerMemo(models.Model):
    id              = models.BigAutoField(primary_key=True)
    target_id       = models.BigIntegerField()
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    memo            = models.TextField(blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'manager_memos'
        ordering = ['-id']
from django.db import models

class tbl_proj(models.Model):
    id = models.BigIntegerField(primary_key=True)  # Explicitly define the BigIntegerField for ID
    name = models.CharField(max_length=255)
    img = models.CharField(max_length=100)
    desc = models.TextField(max_length=1000)
    like = models.BigIntegerField(default=0)
    view = models.BigIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    keyword = models.CharField(max_length=100)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name

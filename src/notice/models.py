from django.db import models

# Create your models here.
class Notice(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    notitype = models.TextChoices("NotiType", "JANGHAKNOTICE GENERALNOTICE HAKSANOTICE IPSINOTICE GLOBALNOTICE HAKSULNOTICE SAFENOTICE BUDDHISTEVENT")
    description = models.TextField()
    notice_id = models.IntegerField()
    date = models.DateField()



from django.db import models

# Create your models here.
class Notice(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    notitype = models.CharField(max_length=30)
        
        # "NotiType", "JANGHAKNOTICE GENERALNOTICE HAKSANOTICE IPSINOTICE GLOBALNOTICE HAKSULNOTICE SAFENOTICE BUDDHISTEVENT")
    description = models.TextField()
    notice_id = models.IntegerField()
    date = models.DateField()
    tdindex = models.TextField() #타이틀+내용 같이있는 텍스트



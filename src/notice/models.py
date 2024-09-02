from django.db import models

class Notice(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    notitype = models.CharField(max_length=30)

        # "NotiType", "JANGHAKNOTICE GENERALNOTICE HAKSANOTICE IPSINOTICE GLOBALNOTICE HAKSULNOTICE SAFENOTICE BUDDHISTEVENT")
    description = models.TextField()
    notice_id = models.IntegerField()
    date = models.DateField()
    tdindex = models.TextField() #타이틀+내용 같이있는 텍스트
    imgs = models.JSONField()
    links = models.JSONField()
    attachments = models.JSONField()
    base_url = models.URLField()
    univ_code = models.CharField(max_length=50) # 학교 코드
    org_code = models.CharField(max_length=50) # 부속기관|단과대 코드
    sub_code = models.CharField(max_length=50) # 부속시설|학과 코드

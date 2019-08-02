import uuid, datetime
from django.db      import models
from account.models import User


# 게시글 이미지 업로드
def user_attach_path(instance, filename):
    today_date = str(datetime.datetime.today().date())
    year    = today_date.split('-')[0]
    month   = today_date.split('-')[1]
    day     = today_date.split('-')[2]

    extention_split = filename.split(".")
    extention = extention_split[extention_split.__len__() - 1]
    return 'attachment/{0}/{1}/{2}/{3}.{4}'.format(year, month, day, uuid.uuid4(), extention)


# 첨부파일 모델
class FileAttachment(models.Model):
    id              = models.BigAutoField(primary_key=True)
    files           = models.FileField(upload_to=user_attach_path, blank=True, null=True)
    file_name       = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'boards_file_attach'


# FAQ 카테고리 모델
class FaqCategory(models.Model):
    id              = models.BigAutoField(primary_key=True)
    category        = models.CharField(max_length=20)
    category_id     = models.BigIntegerField()
    lang            = models.CharField(max_length=10)
    class Meta:
        unique_together = ('category_id', 'lang')
        db_table = 'boards_faq_category'


# FAQ 모델
class Faq(models.Model):
    id              = models.BigAutoField(primary_key=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    faq_category_id = models.BigIntegerField()                              # faq 항목 구분
    title           = models.CharField(max_length=255)
    contents        = models.TextField()
    read_count      = models.BigIntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'boards_faq'


# FAQ 게시물 언어
class FaqLanguage(models.Model):
    id              = models.BigAutoField(primary_key=True)
    board           = models.ForeignKey(Faq, related_name='language', on_delete=models.CASCADE)
    lang            = models.CharField(max_length=50)
    class Meta:
        db_table = 'boards_faq_language'


# 공지사항 모델
class Notice(models.Model):
    id              = models.BigAutoField(primary_key=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    notice          = models.BooleanField(default=0)                                        # 긴급공지 구분
    send_sms        = models.BooleanField(default=0)
    send_email      = models.BooleanField(default=0)
    status          = models.CharField(max_length=50, default='ing')
    title           = models.CharField(max_length=255, blank=True, null=True)
    contents        = models.TextField(blank=True, null=True)
    read_count      = models.BigIntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'boards_notice'


# 공지사항 맵핑 모델
class NoticeFileMap(models.Model):
    id          = models.BigAutoField(primary_key = True)
    board       = models.ForeignKey(Notice, related_name='file_attach', on_delete=models.CASCADE)
    file_info   = models.ForeignKey(FileAttachment, related_name='mapping_notice', on_delete=models.CASCADE)

    class Meta:
        db_table = 'boards_notice_mapping'


# 공지사항 게시물 언어
class NoticeLanguage(models.Model):
    id              = models.BigAutoField(primary_key=True)
    board           = models.ForeignKey(Notice, related_name='language', on_delete=models.CASCADE)
    lang            = models.CharField(max_length=50)
    class Meta:
        db_table = 'boards_notice_language'


# Daily뉴스 모델
class DailyNews(models.Model):
    id              = models.BigAutoField(primary_key=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    status          = models.CharField(max_length=50, default='ing')
    title           = models.CharField(max_length=255, blank=True, null=True)
    contents        = models.TextField(blank=True, null=True)
    source          = models.CharField(max_length=255, blank=True, null=True)
    summary         = models.CharField(max_length=255, blank=True, null=True)
    read_count      = models.BigIntegerField(default=0)
    primary_image   = models.ForeignKey(FileAttachment, related_name='primary_daily', on_delete=models.SET_NULL, blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'boards_daily'


# Daily뉴스 맵핑 모델
class DailyNewsFileMap(models.Model):
    id          = models.BigAutoField(primary_key = True)
    board       = models.ForeignKey(DailyNews, related_name='file_attach', on_delete=models.CASCADE)
    file_info   = models.ForeignKey(FileAttachment, related_name='mapping_daily', on_delete=models.CASCADE)

    class Meta:
        db_table = 'boards_daily_mapping'


# Daily뉴스 게시물 언어
class DailyNewsLanguage(models.Model):
    id              = models.BigAutoField(primary_key=True)
    board           = models.ForeignKey(DailyNews, related_name='language', on_delete=models.CASCADE)
    lang            = models.CharField(max_length=50)
    class Meta:
        db_table = 'boards_daily_language'


# 코인가이드 모델
class CoinGuide(models.Model):
    id              = models.BigAutoField(primary_key=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    status          = models.CharField(max_length=50, default='ing')
    currency        = models.CharField(max_length=30, blank=True, null=True, unique=True)
    title           = models.CharField(max_length=255, blank=True, null=True)
    contents        = models.TextField(blank=True, null=True)
    name_ko         = models.CharField(max_length=50, blank=True, null=True)
    name_en         = models.CharField(max_length=50, blank=True, null=True)
    abbr            = models.CharField(max_length=10, blank=True, null=True)
    developer       = models.CharField(max_length=100, blank=True, null=True)
    algorithm       = models.CharField(max_length=50, blank=True, null=True)
    release_date    = models.DateField(blank=True, null=True)
    block_time      = models.CharField(max_length=100, blank=True, null=True)
    rewards         = models.FloatField(blank=True, null=True)
    total_volume    = models.IntegerField(blank=True, null=True)
    feature         = models.CharField(max_length=255, blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    logo            = models.ForeignKey(FileAttachment, related_name='logo_coinguide', on_delete=models.SET_NULL, blank=True, null=True)
    icon            = models.ForeignKey(FileAttachment, related_name='icon_coinguide', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'boards_coinguide'


# 코인가이드 게시물 언어
class CoinGuideLanguage(models.Model):
    id              = models.BigAutoField(primary_key=True)
    board           = models.ForeignKey(CoinGuide, related_name='language', on_delete=models.CASCADE)
    lang            = models.CharField(max_length=50)
    class Meta:
        db_table = 'boards_coinguide_language'


# 코인가이드 유용한링크 모델
class CoinGuideUsefulLink(models.Model):
    id              = models.BigAutoField(primary_key=True)
    post            = models.ForeignKey(CoinGuide, related_name='link', on_delete=models.CASCADE)
    link            = models.TextField(blank=True, null=True)
    name            = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'boards_coinguide_link'

import uuid, datetime
from django.db      import models
from account.models import User


# 1:1 질문 첨부 경로
def user_attach_path(instance, filename):
    today_date = str(datetime.datetime.today().date())
    year    = today_date.split('-')[0]
    month   = today_date.split('-')[1]
    day     = today_date.split('-')[2]

    extention_split = filename.split(".")
    extention = extention_split[extention_split.__len__() - 1]
    return 'support/{0}/{1}/{2}/{3}.{4}'.format(year, month, day, uuid.uuid4(), extention)


# 첨부파일 모델
class FileAttachment(models.Model):
    id              = models.BigAutoField(primary_key=True)
    files           = models.ImageField(upload_to=user_attach_path, blank=True, null=True)
    file_name       = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'support_attach'


# 1:1 질문 분류
class QuestionType(models.Model):
    id          = models.BigAutoField(primary_key=True)
    type        = models.CharField(max_length=255)
    category_id = models.BigIntegerField()
    lang        = models.CharField(max_length=10)

    class Meta:
        db_table = 'support_questions_type'


# 1:1 질문 모델
class Question(models.Model):
    id              = models.BigAutoField(primary_key=True)
    member_id       = models.BigIntegerField(null=True)                     # 거래소 회원
    question_type_id= models.BigIntegerField()
    status          = models.CharField(max_length=10)
    title           = models.CharField(max_length=255)
    contents        = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'support_questions'

# 1:1 답변 모델
class Answer(models.Model):
    id          = models.BigAutoField(primary_key=True)
    user        = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)     # 백오피스 사용자
    target      = models.ForeignKey(Question, related_name='answer', on_delete=models.CASCADE) # 해당질문 번호
    contents    = models.TextField(null=True)
    locale      = models.CharField(max_length=20, blank=False, null=False, default='ko')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'support_answers'


# 1:1 질문 rawquery 모델
class QuestionRaw(models.Model):
    id = models.IntegerField(primary_key=True)
    member_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    contents = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    question_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    emp_no = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
from rest_framework import serializers

from becoin.model import Members
from .models import (
    Question
    , Answer
    , QuestionType
    , FileAttachment
    , QuestionRaw
)
from account.models import User
from account.serializers import UserAuthSerializer


# 첨부파일 시리얼라이저
class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAttachment
        fields = [
            'id'
            , 'files'
            , 'file_name'
        ]


# 첨부파일 업로드
class FileAttachmentCreateSerializer(serializers.Serializer):
    files       = serializers.FileField()
    file_name   = serializers.CharField()

    def create(self, validated_data):
        files       = validated_data['files']
        file_name   = validated_data['file_name']

        attach_obj = FileAttachment (
            files       = files
            , file_name = file_name
        )

        attach_obj.save()
        return attach_obj


class QuestionAnswerSerializer(serializers.ModelSerializer):
    user    = serializers.SlugRelatedField(many=False
                                            , read_only=True
                                            , slug_field='email')

    class Meta:
        model = Answer
        fields = [
            'id'
            , 'user'
            , 'contents'
            , 'locale'
            , 'created_at'
            , 'updated_at'
        ]


# 1:1 문의 내역 시리얼라이저
class QuestionSerializer(serializers.ModelSerializer):
    answer  = QuestionAnswerSerializer(many=True, read_only=True)
    question_type = serializers.SlugRelatedField(many=False, read_only=True, slug_field='type')
    
    class Meta:
        model = QuestionRaw
        fields = [
            'id'
            , 'member_id'
            , 'question_type'
            , 'question_type_id'
            , 'status'
            , 'title'
            , 'contents'
            , 'created_at'
            , 'updated_at'
            , 'user_id'
            , 'emp_no'
            , 'answer'
        ]


# 1:1 문의 내역 상세조회 / 답변 처리상태 시리얼라이저
class QuestionStateSerializer(serializers.ModelSerializer):
    answer  = QuestionAnswerSerializer(many=True, read_only=True)
    question_type = serializers.SlugRelatedField(many=False, read_only=True, slug_field='type')

    class Meta:
        model = Question
        fields = [
            'id'
            , 'member_id'
            , 'question_type'
            , 'question_type_id'
            , 'status'
            , 'title'
            , 'contents'
            , 'created_at'
            , 'updated_at'
            , 'answer'
        ]

# 1:1 문의내역 작성 시리얼라이저
class QuestionCreateSerializer(serializers.Serializer):
    member_id           = serializers.IntegerField()
    status              = serializers.CharField()
    title               = serializers.CharField(required=True)
    contents            = serializers.CharField(required=True)
    question_type_id    = serializers.IntegerField()

    
    def create(self, validated_data):
        member_id           = validated_data['member_id']
        status              = validated_data['status']
        title               = validated_data['title']
        contents            = validated_data['contents']
        question_type_id    = validated_data['question_type_id']

        question_obj = Question(
            member_id           = member_id
            , status            = status
            , title             = title
            , contents          = contents
            , question_type_id  = question_type_id
        )

        question_obj.save()
        return question_obj


# 1:1 답변 내역 시리얼라이저
class AnswerSerializer(serializers.ModelSerializer):
    user    = UserAuthSerializer
    target  = QuestionSerializer

    class Meta:
        model = Answer
        fields = [
            'id'
            , 'user'
            , 'target'
            , 'contents'
            , 'locale'
            , 'created_at'
            , 'updated_at'
        ]


# 1:1 문의내역 카테고리 시리얼라이저
class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = [
            'id'
            , 'type'
            , 'category_id'
            , 'lang'
        ]
from django.conf import settings

from rest_framework import serializers

from .models import (
    FileAttachment
    , FaqCategory
    , Faq
    , FaqLanguage
    , Notice
    , NoticeLanguage
    , NoticeFileMap
    , DailyNews
    , DailyNewsLanguage
    , DailyNewsFileMap
    , CoinGuide
    , CoinGuideLanguage
    , CoinGuideUsefulLink
)
from account.models import User


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


# FAQ 카테고리 시리얼라이저
class FaqCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqCategory
        fields = [
            'id'
            , 'category'
            , 'category_id'
            , 'lang'
        ]


# FAQ 언어 시리얼라이저
class FaqLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqLanguage
        fields = [
            'id'
            , 'board_id'
            , 'lang'
        ]


# FAQ 언어 작성 시리얼라이저
class FaqLanguageCreatedSerializer(serializers.Serializer):
    board_id    = serializers.IntegerField(required = True)
    lang        = serializers.CharField()

    def create(self, validated_data):
        board_id            = validated_data['board_id']
        lang                = validated_data['lang']

        faq_language_obj = FaqLanguage (
            board_id            = board_id
            , lang              = lang
        )

        faq_language_obj.save()
        return faq_language_obj


# FAQ 목록 시리얼라이저
class FaqSerializer(serializers.ModelSerializer):
    user            = serializers.SlugRelatedField(many=False, read_only=True, slug_field='emp_no')
    language        = FaqLanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Faq
        fields = [
            'id'
            , 'title'
            , 'contents'
            , 'read_count'
            , 'created_at'
            , 'updated_at'
            , 'user_id'
            , 'user'
            , 'faq_category_id'
            , 'language'
        ]


# FAQ 작성 시리얼라이저
class FaqCreateSerializer(serializers.Serializer):
    user_id             = serializers.IntegerField()
    faq_category_id     = serializers.IntegerField()
    title               = serializers.CharField(required=True)
    contents            = serializers.CharField(required=True)

    def create(self, validated_data):
        user_id             = validated_data['user_id']
        faq_category_id     = validated_data['faq_category_id']
        title               = validated_data['title']
        contents            = validated_data['contents']

        faq_obj = Faq(
            user_id             = user_id
            , faq_category_id   = faq_category_id
            , title             = title
            , contents          = contents
        )

        faq_obj.save()
        return faq_obj


# 공지사항 첨부파일 맵핑 시리얼라이저
class NoticeMappingSerializer(serializers.ModelSerializer):
    file_info = FileAttachmentSerializer()
    class Meta:
        model = NoticeFileMap
        fields = [
            'id'
            , 'file_info'
        ]


# 공지사항 첨부파일 맵핑 작성 시리얼라이저
class NoticeMappingCreateSerializer(serializers.Serializer):
    board_id     = serializers.IntegerField()
    file_info_id = serializers.IntegerField()

    def create(self, validated_data):
        board_id     = validated_data['board_id']
        file_info_id = validated_data['file_info_id']

        notice_map_obj = NoticeFileMap (
            board_id        = board_id
            , file_info_id  = file_info_id
        )

        notice_map_obj.save()
        return notice_map_obj


# 공지사항 언어 시리얼라이저
class NoticeLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeLanguage
        fields = [
            'id'
            , 'board_id'
            , 'lang'
        ]


# 공지사항 언어 작성 시리얼라이저
class NoticeLanguageCreateSerializer(serializers.Serializer):
    board_id    = serializers.IntegerField(required = True)
    lang        = serializers.CharField()

    def create(self, validated_data):
        board_id            = validated_data['board_id']
        lang                = validated_data['lang']

        notice_language_obj = NoticeLanguage (
            board_id            = board_id
            , lang              = lang
        )

        notice_language_obj.save()
        return notice_language_obj


# 공지사항 목록 시리얼라이저
class NoticeSerializer(serializers.ModelSerializer):
    user         = serializers.SlugRelatedField(many=False, read_only=True, slug_field='emp_no')
    file_attach  = NoticeMappingSerializer(many=True, read_only=True)
    language     = NoticeLanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Notice
        fields = [
            'id'
            , 'notice'
            , 'send_sms'
            , 'send_email'
            , 'status'
            , 'title'
            , 'contents'
            , 'read_count'
            , 'created_at'
            , 'updated_at'
            , 'user_id'
            , 'user'
            , 'file_attach'
            , 'language'
        ]


# 공지사항 작성 시리얼라이저
class NoticeCreateSerializer(serializers.Serializer):
    user_id         = serializers.IntegerField()

    def create(self, validated_data):
        user_id     = validated_data['user_id']

        notice_obj = Notice (
            user_id = user_id
        )
        
        notice_obj.save()
        return notice_obj


# Daily뉴스 첨부파일 맵핑 시리얼라이저
class DailyNewsMappingSerializer(serializers.ModelSerializer):
    file_info = FileAttachmentSerializer()
    class Meta:
        model = DailyNewsFileMap
        fields = [
            'id'
            , 'file_info'
        ]


# Daily뉴스 첨부파일 맵핑 작성 시리얼라이저
class DailyNewsMappingCreateSerializer(serializers.Serializer):
    board_id     = serializers.IntegerField()
    file_info_id = serializers.IntegerField()

    def create(self, validated_data):
        board_id     = validated_data['board_id']
        file_info_id = validated_data['file_info_id']

        daliy_map_obj = DailyNewsFileMap (
            board_id        = board_id
            , file_info_id  = file_info_id
        )

        daliy_map_obj.save()
        return daliy_map_obj


# Daily뉴스 언어 시리얼라이저
class DailyNewsLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyNewsLanguage
        fields = [
            'id'
            , 'lang'
        ]


# Daily뉴스 언어 작성 시리얼라이저
class DailyNewsLanguageCreateSerializer(serializers.Serializer):
    board_id    = serializers.IntegerField(required = True)
    lang        = serializers.CharField()

    def create(self, validated_data):
        board_id            = validated_data['board_id']
        lang                = validated_data['lang']

        daily_language_obj = DailyNewsLanguage (
            board_id            = board_id
            , lang              = lang
        )

        daily_language_obj.save()
        return daily_language_obj


# Daily뉴스 목록 시리얼라이저
class DailyNewsSerializer(serializers.ModelSerializer):
    user                = serializers.SlugRelatedField(many=False, read_only=True, slug_field='emp_no')
    primary_image       = FileAttachmentSerializer(many=False, read_only=True)
    file_attach         = DailyNewsMappingSerializer(many=True, read_only=True)
    language            = DailyNewsLanguageSerializer(many=True, read_only=True)

    class Meta:
        model = DailyNews
        fields = [
            'id'
            , 'status'
            , 'title'
            , 'contents'
            , 'source'
            , 'summary'
            , 'read_count'
            , 'created_at'
            , 'updated_at'
            , 'user_id'
            , 'user'
            , 'primary_image'
            , 'primary_image_id'
            , 'file_attach'
            , 'language'
        ]


# Daily뉴스 작성 시리얼라이저
class DailyNewsCreateSerializer(serializers.Serializer):
    user_id             = serializers.IntegerField()

    def create(self, validated_data):
        user_id         = validated_data['user_id']

        news_obj = DailyNews (
            user_id = user_id
        )
        
        news_obj.save()
        return news_obj


# 코인가이드 언어 시리얼라이저
class CoinGuideLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinGuideLanguage
        fields = [
            'id'
            , 'board_id'
            , 'lang'
        ]


# 코인가이드 언어 작성 시리얼라이저
class CoinGuideLanguageCreateSerializer(serializers.Serializer):
    board_id    = serializers.IntegerField(required = True)
    lang        = serializers.CharField()

    def create(self, validated_data):
        board_id            = validated_data['board_id']
        lang                = validated_data['lang']

        coinguide_language_obj = CoinGuideLanguage (
            board_id            = board_id
            , lang              = lang
        )

        coinguide_language_obj.save()
        return coinguide_language_obj


# 코인가이드 유용한링크 시리얼라이저
class CoinGuideUsefulLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinGuideUsefulLink
        fields = [
            'id'
            , 'post'
            , 'link'
            , 'name'
        ]

# 코인가이드 유용한링크 작성 시리얼라이저
class CoinGuideUsefulLinkCreateSerializer(serializers.Serializer):
    post_id     = serializers.IntegerField()
    link        = serializers.CharField()
    name        = serializers.CharField()

    def create(self, validated_data):
        post_id             = validated_data['post_id']
        link                = validated_data['link']
        name                = validated_data['name']

        coinguide_link_obj = CoinGuideUsefulLink (
            post_id         = post_id
            , link          = link
            , name          = name
        )

        coinguide_link_obj.save()
        return coinguide_link_obj


# 코인가이드 목록 시리얼라이저
class CoinGuideSerializer(serializers.ModelSerializer):
    user          = serializers.SlugRelatedField(many=False, read_only=True, slug_field='emp_no')
    logo          = FileAttachmentSerializer(many=False, read_only=True)
    icon          = FileAttachmentSerializer(many=False, read_only=True)
    language      = CoinGuideLanguageSerializer(many=True, read_only=True)
    link          = CoinGuideUsefulLinkSerializer(many=True, read_only=True)

    class Meta:
        model = CoinGuide
        fields = [
            'id'
            , 'user'
            , 'user_id'
            , 'status'
            , 'currency'
            , 'title'
            , 'contents'
            , 'name_ko'
            , 'name_en'
            , 'abbr'
            , 'developer'
            , 'algorithm'
            , 'release_date'
            , 'block_time'
            , 'rewards'
            , 'total_volume'
            , 'feature'
            , 'created_at'
            , 'updated_at'
            , 'logo'
            , 'icon'
            , 'language'
            , 'link'
        ]


# 코인가이드 작성 시리얼라이저
class CoinGuideCreateSerializer(serializers.Serializer):
    user_id             = serializers.IntegerField()

    def create(self, validated_data):
        user_id         = validated_data['user_id']

        news_obj = CoinGuide (
            user_id = user_id
        )
        
        news_obj.save()
        return news_obj
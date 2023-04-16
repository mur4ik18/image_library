from posts.models import Post, Tag
from posts_collections.models import Collection
from rest_framework import serializers
from django.contrib.auth.models import User


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields=[
            'tag_name'
        ]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title']


class PostsSerializer(serializers.ModelSerializer):
    postID = serializers.SerializerMethodField('_postid')
    custom_image = serializers.SerializerMethodField('_custom_image')
    tags = TagsSerializer(many=True, default='')
    collections = CollectionSerializer(many=True, default='')
    edit = serializers.SerializerMethodField('_edit')
    account_link = serializers.SerializerMethodField('_account_link')

    class Meta:
        model = Post
        fields = [
            'postID',
            'author',
            'post_url',
            'custom_image',
            'date',
            'likes',
            'comments',
            'caption',
            'hashtags',
            'mentions',
            'text_comments',
            'image_field',
            'tags',
            'alt_name',
            'file_name',
            'collections',
            'edit',
            'account_link'
        ]

    def _account_link(self, obj):
        if obj.website == "0":
            return f'https://www.instagram.com/{obj.author}/'
        else:
            return obj.website

    def _edit(self, obj):
        return 1 if obj.edited else 0

    def _postid(self, obj):
        return str(obj.image).split('/')[-1].split('.jpg')[0]

    def _custom_image(self, obj):
        return f"http://127.0.0.1/images/{obj.image}"


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username'
        ]

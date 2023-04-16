from posts.models import Post
from posts_collections.models import Collection
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title']


class PostsSerializer(serializers.ModelSerializer):
    collections = CollectionSerializer(many=True, default='')

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'image',
            'image_field',
            'collections',
            'ai_caption',
            'ai_description',
        ]

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related('posts')
        return queryset

from rest_framework import serializers


from .models import Post

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'short_description',
            'full_description',
            'main_picture',
            'published_date'
        )

# class PostDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = [
#             'id',
#             'title',
#             'short_description',
#             'full_description',
#             'main_picture',
#             'published_date'
#         ]

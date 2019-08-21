from rest_framework import serializers


from .models import Post

class PostSerializer(serializers.HyperlinkedModelSerializer):
    image_urls = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'subtitle',
            'short_description',
            'full_description',
            'main_picture',
            'published_date',
            'image_urls',
        )

    def get_image_urls(self, obj):
        if obj.main_picture:
            request = self.context.get('request')
            thumbnail_url = request.build_absolute_uri(obj.main_picture.thumbnail.url)
            medium_url = request.build_absolute_uri(obj.main_picture.medium.url)
            large_url = request.build_absolute_uri(obj.main_picture.large.url)
            image_urls = dict({
                'thumbnail': thumbnail_url,
                'medium': medium_url,
                'large': large_url
                })
            # import pdb; pdb.set_trace()
            return image_urls
        else:
            return None



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

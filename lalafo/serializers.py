from rest_framework import serializers

from lalafo.models import Lalafo, Comment, Favourite, Rating


class LalafoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lalafo
        fields = ('id', 'title', 'description', 'user', 'image',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.count()
        return rep


class LalafoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lalafo
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Lalafo.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'rate', 'post', 'user')

    def validate(self, attrs):
        post = attrs.get('post')
        request = self.context.get('request')
        user = request.user
        if Rating.objects.filter(post=post, user=user).exists():
            raise serializers.ValidationError('Невозможно рейтинг ставить дважды')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class FavouriteLalafoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = ('post', 'id')

        def get_favourite(self, obj, request):
            if obj.favourite and request.user and request.user == obj.user:
                return obj.favourite
            return ''

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['favourite'] = self.get_favourite(instance)
            return rep


class CreateLalafoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lalafo
        exclude = ('user', )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(write_only=True,
                                              queryset=Lalafo.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('user', 'text', 'post',)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)




from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.models import User
from reviews.models import Category, Genre, Title, Review, Comment
from rest_framework.relations import SlugRelatedField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("first_name", "last_name", "username", "bio", "email", "role")
        model = User
        read_only_field = ("role",)


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(
        required=True, max_length=150, regex="^[\\w.@+-]+\\Z"
    )

    def validate(self, data):
        if self.initial_data.get("username") == "me":
            raise serializers.ValidationError(
                {"username": ["Вы не можете использоват этот username!"]}
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all(), required=True
    )

    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True, required=True
    )

    class Meta:
        model = Title
        fields = "__all__"


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        fields = "__all__"
        model = Title
        read_only_fields = ("__all__",)


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    def get_title(self):
        title_id = self.context.get("view").kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return title

    def validate(self, data):
        if self.context.get("request").method != "POST":
            return data
        title = self.get_title()
        user = self.context.get("request").user
        if Review.objects.filter(title=title, author=user).exists():
            raise serializers.ValidationError("Entry Already exists!")
        return data

    class Meta:
        model = Review
        fields = (
            "id",
            "pub_date",
            "text",
            "author",
            "score",
        )


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "pub_date",
            "text",
            "author",
        )

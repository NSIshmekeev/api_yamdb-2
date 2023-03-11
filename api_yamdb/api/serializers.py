from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User
        read_only_field = ('role',)


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(required=True, max_length=150,
                                      regex='^[\\w.@+-]+\\Z')

    def validate(self, data):
        if self.initial_data.get('username') == 'me':
            raise serializers.ValidationError(
                {"username": ["Вы не можете использоват этот username!"]}
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

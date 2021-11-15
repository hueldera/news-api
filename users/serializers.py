from rest_framework.serializers import ModelSerializer, CharField
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(ModelSerializer):

    password = CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
        )

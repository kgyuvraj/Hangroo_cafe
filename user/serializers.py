from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from user.models import   \
     Gender, Avatar, Country

User = get_user_model()


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = "__all__"


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = "__all__"


class CreateUserSerializer(serializers.ModelSerializer):
    avatar = PrimaryKeyRelatedField(required=False,
        many=False, queryset=Avatar.objects.all())
    gender = PrimaryKeyRelatedField(
        many=False, queryset=Gender.objects.all())
    country = PrimaryKeyRelatedField(
        many=False, queryset=Country.objects.all())
        
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {
                "write_only": True
                }
            }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        
        instance.dob = validated_data.get('dob', instance.dob)
        instance.email = validated_data.get('email', instance.email)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance

###Do not remove required as part of framework
class UserSerializer(serializers.ModelSerializer):
    avatar = PrimaryKeyRelatedField(required=False,
        many=False, queryset=Avatar.objects.all())
    gender = PrimaryKeyRelatedField(required=False,
        many=False, queryset=Gender.objects.all())
    country = PrimaryKeyRelatedField(required=False,
        many=False, queryset=Country.objects.all())
        
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password':{
                "write_only": True,
                "required": False
                },
            'username':{
                "required": False
                },
            'phone':{
                "required": False
                },
            }


class UpdateUserSerializer(serializers.ModelSerializer):
    avatar = PrimaryKeyRelatedField(required=False,
        many=False, queryset=Avatar.objects.all())
    gender = PrimaryKeyRelatedField(required=False,
        many=False, queryset=Gender.objects.all())
    country = PrimaryKeyRelatedField(required=False,
        many=False, queryset=Country.objects.all())
        
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password':{
                "write_only": True,
                "required": False
                },
            'username':{
                "required": False
                },
            'phone':{
                "required": False
                },
            }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        
        instance.dob = validated_data.get('dob', instance.dob)
        instance.email = validated_data.get('email', instance.email)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        
        instance.gender = validated_data.get('gender', instance.gender)
        
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        if phone and password:
            user = authenticate(request=self.context.get('request'),
                                phone=phone, password=password)

            # The authenticate call simply returns None for is_active=False
            # user. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "phone" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


class PublicUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("avatar", "username", "id", "bio" )
        

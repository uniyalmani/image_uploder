from rest_framework import serializers
from auth_app.models import User

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'},
                                             write_only = True)
    class Meta:
        model = User
        fields = ['name','email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }



    def validate(self, attrs):
        print(attrs, "llllllllll")
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm password dose not match")
        # del attrs["confirm_password"]
        print(attrs, "llllllllll")
        return attrs
    
    def create(self, validated_data):

        return User.objects.create_user(**validated_data)
    

class UserLoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']
from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        
    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']
        email = self.validated_data['email']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error': 'P1 and P2 should be the same'})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})
        
        account = User(username=username, email=email)
        account.set_password(password)
        account.save()
        
        return account
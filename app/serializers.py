from rest_framework import serializers
from .models import User, Files, Download_History

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user

        
        if user.is_authenticated and user.user_type == 'client':
            data.pop('special_token', None)

        return data

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'

class Download_HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Download_History
        fields = '__all__'

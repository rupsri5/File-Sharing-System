from rest_framework import serializers
from .models import User, Files

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
    filename=serializers.CharField(required=False)
   
    class Meta:
        model=Files
        fields=['id','filename','file','upload_date','user_id_upload','user_id_delete','file_type', 'file_present']
        
    def validate(self, data):
        mandatory_fields=set(['file', 'file_present'])
        extra_fields = set(data.keys())-mandatory_fields
        
        if extra_fields:
            raise serializers.ValidationError(f"Extra Fields provided: [{', '.join(extra_fields)}]")
        if not mandatory_fields.issubset(data.keys()):
            raise serializers.ValidationError("file and user_id_upload are mandatory")  
        if data['file'].split('.')[-1].lower() not in [file_type[0] for file_type in Files.FILE_TYPE]:
            raise serializers.ValidationError("Invalid file type")
        return data 
            

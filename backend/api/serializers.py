from rest_framework import serializers
from .models import Company, MOU, Clause

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class MOUSerializer(serializers.ModelSerializer):
    class Meta:
        model = MOU
        fields = '__all__'

class ClauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clause
        fields = '__all__'

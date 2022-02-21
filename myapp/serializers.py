"""Serialization libraries"""
from rest_framework import serializers
from rest_framework.response import Response
from . models import person

"""Serialization"""
class PrSerializer(serializers.Serializer):

	name=serializers.CharField(max_length=10)
	age= serializers.IntegerField()
	job_type = serializers.CharField(max_length = 10)
	address = serializers.CharField(max_length = 100)

	def create(self, validate_data):
		return person.objects.create(**validate_data)

	def update(self,instance,validated_data):
		instance.name = validated_data.get('name', instance.name)
		instance.age = validated_data.get('age', instance.age)
		instance.job_type = validated_data.get('job_type', instance.job_type)
		instance.address = validated_data.get('address', instance.address)
		instance.save()
		return instance
	
	def delete(self,instance):
		instance.delete()



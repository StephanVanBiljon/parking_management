from rest_framework import serializers
from .models import Client, ParkingUser, LicencePlate
from django.contrib.auth.hashers import make_password

class ClientRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['username', 'password', 'email', 'address']

    def create(self, validated_data):
        validated_data['is_staff'] = True
        # Hash the password
        validated_data['password'] = make_password(validated_data['password'])

        return Client.objects.create(**validated_data)

class LicencePlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicencePlate
        fields = ['licence_plate', 'region']

class ParkingUserSerializer(serializers.ModelSerializer):
    licence_plates = LicencePlateSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = ParkingUser
        fields = ['email', 'first_name', 'last_name', 'licence_plates', 'client']

    def create(self, validated_data):
        plates_data = validated_data.pop('licence_plates', [])
        parking_user = ParkingUser.objects.create(**validated_data)

        for plate in plates_data:
            LicencePlate.objects.create(
                parking_user=parking_user,
                **plate
            )

        return parking_user

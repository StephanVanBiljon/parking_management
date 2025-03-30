from rest_framework import generics, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from .models import ParkingUser
from .serializers import ClientRegistrationSerializer, ParkingUserSerializer
import pandas as pd
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

Client = get_user_model()


class ClientRegistrationView(generics.CreateAPIView):
    """
    API endpoint for client registration.
    """
    serializer_class = ClientRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class ClientLoginView(ObtainAuthToken):
    """
    API endpoint for client login.
    Returns an authentication token upon successful login.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class ClientLogoutView(APIView):
    """
    API endpoint for client logout.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK
        )

class ParkingUserViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing parking users.
    """
    serializer_class = ParkingUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        """
        Ensure clients can only see their own users.
        """
        return ParkingUser.objects.filter(client=self.request.user)

    @action(detail=False, methods=['post'])
    def bulk_import(self, request):
        """
        Endpoint for bulk importing users from Excel or CSV files.
        Format: email, first_name, last_name, license_plate, region
        """
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']

        try:
            # Determine file type and read accordingly.
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xlsx')):
                df = pd.read_excel(file)
            else:
                return Response({'error': 'Unsupported file format. Please upload CSV or Excel file.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Validate required columns
            required_cols = ['email', 'first_name', 'last_name', 'license_plate', 'region']
            missing_cols = [col for col in required_cols if col not in df.columns]

            if missing_cols:
                return Response({
                    'error': f'Missing required columns: {", ".join(missing_cols)}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Process the data
            created_count = 0
            errors = []

            for idx, row in df.iterrows():
                try:
                    # Prepare data for ParkingUserSerializer
                    parking_user_data = {
                        'email': row['email'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'licence_plates': [{
                            'licence_plate': str(row['license_plate']),
                            'region': row['region'],
                        }],
                        'client': request.user.id
                    }

                    serializer = ParkingUserSerializer(data=parking_user_data)

                    if serializer.is_valid():
                        serializer.save()
                        created_count += 1
                    else:
                        errors.append(f"Row {idx + 1}: {serializer.errors}")

                except Exception as e:
                    errors.append(f"Row {idx + 1}: {str(e)}")

            return Response({
                'message': f'Successfully imported {created_count} users',
                'errors': errors if errors else None
            }, status=status.HTTP_201_CREATED if created_count > 0 else status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

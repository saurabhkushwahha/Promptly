from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

# Import the serializers for request and response validation
from .serializers import PromptSerializer, ResponseSerializer

# Import the function that processes the AI prompt
from ai.main import process_promptly_ai



class AIChatAPIView(APIView):
    @extend_schema(
        request=PromptSerializer,
        responses={200: ResponseSerializer},
        description="Send a prompt to the AI and receive a generated response."
    )
    def post(self, request):
        serializer = PromptSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data['prompt']
            file_path = serializer.validated_data.get('file_path')  # This is optional
            ai_response = process_promptly_ai(query=prompt, file_path=file_path)
            return Response({"response": ai_response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

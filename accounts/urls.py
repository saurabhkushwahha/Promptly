from django.urls import path
from accounts.views import (
    AIChatAPIView,
)
urlpatterns = [
    path('chat/', AIChatAPIView.as_view(), name='ai-chat'),
]

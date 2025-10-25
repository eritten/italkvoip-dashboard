from django.urls import path
from .views import GetCredentialsAPIView

app_name = 'api'

urlpatterns = [
    path('credentials/', GetCredentialsAPIView.as_view(), name='get-credentials'),
]

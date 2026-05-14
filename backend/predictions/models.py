from django.db import models

# Create your models here.
from django.db import models
from users.models import User
from core.models import AIModel
from api_keys.models import APIKey

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE)
    input_data = models.TextField()
    output_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
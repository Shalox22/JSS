from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def chatbot(request):
    message = request.data.get("message")

    if "hello" in message.lower():
        reply = "Hello! Welcome to AI Platform."
    elif "model" in message.lower():
        reply = "You can test models from the dashboard."
    else:
        reply = "I am here to guide you."

    return Response({"reply": reply})
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api_keys.models import APIKey

@api_view(['POST'])
def predict(request):
    api_key = request.data.get("api_key")
    input_data = request.data.get("input")

    # 🔐 Validate API Key
    if not APIKey.objects.filter(key=api_key).exists():
        return Response({"error": "Invalid API Key"}, status=403)

    # 🤖 TEMPORARY MODEL LOGIC
    result = f"Processed: {input_data}"

    return Response({
        "input": input_data,
        "result": result
    })
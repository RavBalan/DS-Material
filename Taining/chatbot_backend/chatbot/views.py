from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def chatbot_response(request):
    user_message = request.data.get("message", "").lower()
    
    # Basic responses
    if "hello" in user_message or "hi" in user_message:
        return Response({"response": "Hello! How can I assist you?"})
    elif "how are you" in user_message:
        return Response({"response": "I'm doing great! How about you?"})
    
    # Example custom logic
    if "help" in user_message:
        return Response({"response": "Sure, let me know what you need help with!"})
    
    return Response({"response": "I'm sorry, I don't understand. Can you rephrase?"})

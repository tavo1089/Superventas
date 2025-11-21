from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def whatsapp_webhook(request):
    return HttpResponse('WhatsApp Bot Activado', status=200)

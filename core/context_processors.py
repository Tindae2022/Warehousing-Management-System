from chat.models import MessageNotification
from .models import Notification
def notification_count(request):
    if request.user.is_authenticated:
        return {
            'notification_count': Notification.objects.filter(user=request.user, is_read=False).count()

        }
    return {}




def message_notification_count(request):
    if request.user.is_authenticated:
        return {
            'message_notification_count': MessageNotification.objects.filter(user=request.user, is_read=False).count()
        }
    return {}


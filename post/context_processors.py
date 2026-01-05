from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        return {
            'notifications': Notification.objects.filter(
                to_user=request.user,
                is_read=False
            ).order_by('-created_at')[:5],
            'notifications_count': Notification.objects.filter(
                to_user=request.user,
                is_read=False
            ).count()
        }
    return {}

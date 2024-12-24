from django.http import HttpResponseForbidden
from datetime import timedelta
from django.utils.timezone import now
from .models import FailedLoginAttempt

class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # this part is executed before
        ip_address = self.get_client_ip(request)
        if self.is_blocked(ip_address):
            return HttpResponseForbidden("Your IP is blocked temporarily.")
        
        response = self.get_response(request)
        # this part is executed after the view is processed
        return response

    def get_client_ip(self, request):
        """
        get the client's IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def is_blocked(self, ip):
        """
        if the number of failed login attempts from this IP address is greater than 5 in the last 15 minutes, block it
        """
        cooldown = timedelta(minutes=15)
        try:
            attempt = FailedLoginAttempt.objects.get(ip_address=ip)
            if attempt.attempts >= 5 and now() - attempt.last_attempt < cooldown:
                return True
            elif now() - attempt.last_attempt >= cooldown:
                attempt.attempts = 0
                attempt.save()
        except FailedLoginAttempt.DoesNotExist:
            pass
        return False


from django.conf import settings


CLIENT_ID = getattr(settings, 'EXACT_TARGET_CLIENT_ID', '')
CLIENT_SECRET = getattr(settings, 'EXACT_TARGET_CLIENT_SECRET', '')
WSDL_URL = getattr(settings, 'EXACT_TARGET_WSDL_URL', '')

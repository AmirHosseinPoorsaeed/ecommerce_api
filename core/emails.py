from djoser.email import ActivationEmail
from django.contrib.auth.tokens import default_token_generator
from .tasks import send_activation_email
from django.conf import settings
from djoser import utils
import logging

logger = logging.getLogger(__name__)

class CustomActivationEmail(ActivationEmail):
    
    def send(self, to):

        activation_url = settings.DJOSER.get('ACTIVATION_URL')
        
        context = super().get_context_data()
        user = context.get('user')
        context['uid'] = utils.encode_uid(user.pk)
        context['token'] = default_token_generator.make_token(user)
        context['url'] = activation_url.format(**context)

        send_activation_email.delay(to, context['url'])

        logger.info(f'Activation email sent to {to} with url: {context['url']}')
        
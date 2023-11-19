from config import Secrets
from trycourier import Courier
from trycourier.exceptions import CourierAPIException

class SendEmail:
    def __init__(self):
        self.client = Courier(auth_token=Secrets.COURIER_AUTH_TOKEN)

    def send_email(self, data: dict):

        try:
            self.client.send_message(
                message={
                    "to": [{
                        "email": Secrets.EMAIL_ADMIN,
                    },
                    {
                        "email": data['email_user'],
                    }],
                    "template": Secrets.ID_TEMPLATE_COURIER,
                    "data": {
                        "nombre": data['nombre'],
                        "email": data['email_user'],
                        "mensaje": data['mensaje'],
                        "subject": "Solicitud de Trailers",
                    },
                }
            )
            return ('Email Enviado', 'success')
        
        except CourierAPIException as e:
            raise ErrorSendEmail(f'Error al enviar el correo: {e}')
        
        except Exception as e:
            raise ErrorSendEmail(f'Email NO Enviado: {e}')
        
class ErrorSendEmail(Exception):
    pass

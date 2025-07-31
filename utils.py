# Django models
from django.core.mail import send_mail


class store_activation_info():
    """
    this is class to store account verification and activation info and send activation code to
     users to activate they're account
    """
    def __init__(self, request, phone_number, activation_code):
        self.session = request.session
        self.phone_number = phone_number
        self.activation_code = activation_code

    def store_activation_info_in_session(self):
        if not self.session.get('activation_phone_number'):
            self.session['activation_phone_number'] = self.phone_number
        self.session['activation_phone_number'] = self.phone_number
        subject = 'Activation Code'
        message = f'your Activation code is {self.activation_code} .'
        from_email = 'mmtmmt945@gmail.com'
        recipient_list = [self.phone_number]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        print('========================================')
        print(self.activation_code)
        print('========================================')
        self.session.save()

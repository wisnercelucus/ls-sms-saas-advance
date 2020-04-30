def getShortFromName(name):
    name_parts = name.split(' ')
    short = ''
    name_parts_fisrt_chars = []
    for part in name_parts:
        fisrt_char = part[0]
        name_parts_fisrt_chars.append(fisrt_char)
    short = ''.join(name_parts_fisrt_chars)
    return short.lower()

def generate_randowm_password(length):
    import random
    password_length = length
    possible_characters = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789"
    random_character_list = [random.choice(possible_characters) for i in range(password_length)]
    random_password = "".join(random_character_list)
    return random_password

def email_account_info(
        mail_subject,
        email_template,
        username,
        tenant_domain,
        to_email,
        rand_pass
    ):
    from django.core.mail import EmailMessage
    from django.template.loader import render_to_string
    message = render_to_string(email_template, {
    'user': username,
    'domain': tenant_domain,
    'password': rand_pass,
    'email': to_email,
    })
    to_email = to_email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

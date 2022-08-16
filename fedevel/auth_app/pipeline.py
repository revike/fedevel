def save_user(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        user.is_active_email = False
        user.is_active_phone = False
        user.save()
    if backend.name == 'google-oauth2':
        user.is_active_phone = False
        user.save()

def user_role(request):
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        return {'user_role': request.user.profile.get_role_display()}
    return {'user_role': None}

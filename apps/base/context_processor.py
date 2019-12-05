from apps.whursauth.models import User

def user_information(request):
    std_id = request.session.get('std_id')
    context = {}
    try:
        user = User.objects.get(std_id=std_id)
        if user:
            context['std_id'] = user.std_id
            context['username'] = user.username
    except:
        pass
    return context
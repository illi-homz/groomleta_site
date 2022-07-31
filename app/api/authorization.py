from django.http import JsonResponse
import json
from graphql_jwt.refresh_token.models import RefreshToken


def logout(request):
    # print('request', dir(request))
    token = None

    try:
        data = json.loads(request.body)
        token = data['token']
    except:
        print('token field don\'t exist')
        pass

    if not token:
        return

    # alltokens = RefreshToken.objects.all()
    # print('alltokens', dir(alltokens[0]))
    # print('token', alltokens[0].token)

    current_token = RefreshToken.objects.filter(token=token)
    print('user_all_tokens', dir(current_token))
    r = current_token.delete()
    print('rrrrrrrrrrr', r)

    response = {
        'status': 'success',
        'code': 200,
        'ok': True
    }

    return JsonResponse(response)

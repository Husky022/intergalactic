from authapp.models import IntergalacticUser

def set_user_parameter(data):
    parameter = data['id'].split('-')[0]
    parameter_value = True if data['checked'] == "true" else False
    print(parameter)
    print(parameter_value)
    user = IntergalacticUser.objects.filter(id=data['id'].split('-')[1]).first()
    setattr(user, parameter, parameter_value)
    user.save()


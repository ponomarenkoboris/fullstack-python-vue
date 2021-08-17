import datetime, jwt

def set_jwt(user_id, status):
    """
    Создание JWT токена
    :param user_id: идентификатор пользователя
    :param status: статус авторизации (manger or user)
    :return: JWT token
    """
    payload = {
        'id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow(),
        'status': status
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token

def get_data_from_jwt(token):
    """
    Десериализация JWT токена
    :param token: JWT токен
    :return: payload dict : {
        'id': id,
        'exp': datetime,
        'iat': datetime,
        'status': статус пользователя
        }
    """
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])

    if payload is None:
        return False

    return payload

from models.user import UserModel
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = UserModel.findByUsername(username)
    # safe_str_cmp ---> Supports for older and newer version string comparison
    if user and safe_str_cmp(user.password, password):
        return user
    return None


def identity(payload):
    user_id = payload['identity']
    return UserModel.findById(user_id)


from infrastructure.db.repositories.UsersRepository import UserRepository
from app.use_cases.user_update import UserUpdate

use_case = UserUpdate(UserRepository())

user = use_case.update_user('201.921.902-02', '', '')

print(user)

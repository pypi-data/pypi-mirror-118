SUBMISSION_DEFAULT_URL = 'http://submit.aifactory.solutions'
AUTH_DEFAULT_URL = 'http://auth.aifactory.solutions'

# Authentication method
class AUTH_METHOD:
    USERINFO = 0
    TOKEN = 1
    MAX_TRIAL = 3

class AUTH_RESPONSE:
    NO_AVAILABLE_LAP = 'NO_AVAILABLE_LAP'
    TOKEN_NOT_VALID = 'TOKEN_NOT_VALID'
    TOKEN_EXPIRED = 'TOKEN_EXPIRED'
    DB_NOT_AVAILABLE = 'DB_NOT_AVAILABLE'
    USER_NOT_EXIST = 'USER_NOT_EXIST'
    USER_NOT_PARTICIPATING = 'USER_NOT_PARTICIPATING'
    PASSWORD_NOT_VALID = 'PASSWORD_NOT_VALID'

class DEBUGGING_PARAMETERS:
    TOKEN = "DEBUGGING_TOKEN"
    PASSWORD = 'qlqjs1'

class SUBMIT_RESULT:
    FAIL_TO_SUBMIT = 0
    SUBMIT_SUCCESS = 200

class LOG_TYPE:
    SUBMISSION = 'SUBMISSION_LOG'
    RELEASE = 'RELEASE_LOG'


class AuthServerError(Exception):
    ment = "The auth server has an error. \n"
    ment += "Please ask the system administrator or try submitting later. \n"
    def __str__(self):
        return self.ment

class TaskIDNotAvailableError(Exception):
    ment = "This task doesn't have any available lap. \n"
    ment += "Please check if you have a right task id. \n"
    def __str__(self):
        return self.ment

class UserNotRegisteredError(Exception):
    ment = "This user hasn't registered in this task. \n"
    ment += "Please check if you have registered in this task on our website. \n"
    def __str__(self):
        return self.ment

class AuthMethodNotAvailableError(Exception):
    ment = "This auth method is not available for now. \n"
    ment += "Please check the updated version of aifactory_alpha package. \n"
    def __str__(self):
        return self.ment

class RefreshTokenNotFoundError(Exception):
    ment = "You have to either set AIF_TOKEN environment variable \n \
                or put your submission token as a parameter."
    def __str__(self):
        return self.ment


class UserInfoNotDefinedError(Exception):
    ment = "You must provide `email` or `user_id` to submit your result."
    def __str__(self):
        return self.ment


class TaskIDNotDefinedError(Exception):
    ment = "You must provide `task_id` to submit your result."
    def __str__(self):
        return self.ment


class WrongAuthMethodError(Exception):
    ment = "Wrong Authentification Method. Method should be either AUTH_METHOD.USERINFO or AUTH_METHOD.TOKEN."
    def __str__(self):
        return self.ment


class AuthentificationNotValidError(Exception):
    ment="Information for authentification not enough."
    def __str__(self):
        return self.ment


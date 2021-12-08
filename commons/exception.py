UNKNOWN_ERROR = "X001"
class CustomException(Exception):
    def __init__(self, message):
        self.message = message
        
    
    NO_AWS_ACCOUNT_FOUND = "E001"
    INCORRECT_PHONE_NUMBER_FORMAT = "E002"
    OTP_INCORRECT = "E003"
    OTP_NOT_SENT = "E004"
    OTP_OR_PHONE_INCORRRECT_FORMAT = "E005"
    SERIALIZER_ERROR = "E006"
    PHONE_NOT_VALIDATED = "E007"
    PHONE_OR_PASSWORD_INCORRECT_FORMAT = "E008"
    OTP_LIMIT_EXCEEDED = "E009"
    FAILED_SENDING_OTP = "E010"
    ALREADY_LIKED = "E011"
    BLOG_DOES_NOT_EXIST = "E012"
    BLOG_LIKE_DOES_NOT_EXIST = "E013"
    EMPYT_COMMENT = "E014"
    USER_DOES_NOT_EXIST = "E015"
    ALREADY_FOLLOWED = "E016"
    DUPLICATE_PHONE = "E017"
    NEWSLETTER_ALREADY_SUBSCRIBED = "E018"
    INCORRECT_EMAIL_ID = "E019"
    INVALID_ORDER_ID = "E020"
    USER_PROFILE_NOT_FOUND = "E021"
    def get_exception_messsage(self, exception_code):

        switcher = {
            "E001": "No aws account found with provided details",
            "E002": "Provide the 'phone' in proper format eg: +918285XXXXXX",
            "E003": "OTP incorrcet",
            "E004": "First proceed via sending otp request",
            "E005": "Please provide both otp and phone in correct format for validation",
            "E006": "Please privide the data in correct format",
            "E007": "Please verify phone first",
            "E008": "Atleast phone and password are required in correct format",
            "E009": "Sending otp error limit exceeded, Please contact customer support.",
            "E010": "Error occurred while sending OTP please try after sometime.",
            "E011": "You have already liked this post",
            "E012": "The blog does not exist",
            "E013": "Blog like does not exist",  
            "E014": "Comment can't be empty",
            "E015": "User does not exist",
            "E016": "You are already following this user",
            "E017": "Phone number already exist",
            "E018": "You have already subscribed for the newsletters",
            "E019": "Provided email is incorrect",
            "E020": "Invalid order id",
            "E021": "User does not have a profile. Please ask admin and get a profile created.",
            "X001": "Unknown error occured"
        }
        return switcher.get(exception_code, 'Some error occured')

    
    

from flask import jsonify
import random
import redis
from urllib.parse import quote
import http.client


class Authenticator:
    # Class-level constants
    SMS_USERNAME = "9189629604"
    SMS_APIKEY = "sf2xGcOmQvLuu5BkW5SCcOIrqJdzVKJIfdKMcscEhGrTyhWZ"
    SMS_LINENUMBER = "30007732903082"
    SMS_TEXT = "کاربر گرامی کد تأیید شما: "

    # Redis client initialization
    redis_client = redis.StrictRedis(
        host='localhost', port=6379, db=0, decode_responses=True
    )

    @staticmethod
    def send_sms(phone_number):
        """Sends a verification SMS to the given phone number."""
        # Check if a code is already sent to this number
        if Authenticator.redis_client.exists(f'verification:{phone_number}'):
            return {
                "status": "error",
                "message": "کاربر گرامی، قبلاً برای شما کد ارسال شده است."
            }

        # Generate a new verification code
        verify_code = str(random.randint(100000, 999999))
        message_text = f"{Authenticator.SMS_TEXT}{verify_code}"

        # Prepare the API request
        conn = http.client.HTTPSConnection("api.sms.ir")
        request_url = (
            f"/v1/send?"
            f"username={quote(Authenticator.SMS_USERNAME)}&password={quote(Authenticator.SMS_APIKEY)}&"
            f"mobile={quote(phone_number)}&line={quote(Authenticator.SMS_LINENUMBER)}&"
            f"text={quote(message_text)}"
        )
        headers = {'Accept': 'text/plain'}

        try:
            # Send the request
            conn.request("GET", request_url, '', headers)
            response = conn.getresponse()

            # Handle the response
            if response.status == 200:
                Authenticator.store_verification_code(phone_number, verify_code)
                return {
                    "status": "success",
                    "message": "کد تأیید با موفقیت ارسال شد."
                }
            else:
                return {
                    "status": "error",
                    "message": f"خطا در ارسال کد: {response.read().decode('utf-8')}"
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"خطای ارسال کد: {str(e)}"
            }

    @staticmethod
    def verify_code(phone_number, entered_code):
        """Verifies the entered code against the stored code."""
        # Retrieve the stored verification code
        stored_code = Authenticator.redis_client.get(f'verification:{phone_number}')

        if stored_code is None:
            return {
                "status": "error",
                "message": "کد تأیید یافت نشد یا منقضی شده است."
            }

        # Compare the codes
        if stored_code == entered_code:
            return {
                "status": "success",
                "message": "کد شما تأیید شد."
            }
        else:
            return {
                "status": "error",
                "message": "کد واردشده معتبر نیست."
            }

    @staticmethod
    def store_verification_code(phone_number, verify_code):
        """Stores the verification code in Redis with a 2-minute expiry."""
        Authenticator.redis_client.setex(
            f'verification:{phone_number}', 120, verify_code
        )

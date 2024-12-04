from flask import jsonify
import random
import redis
from urllib.parse import quote
import http.client

class Authenticator:
    """
    A class to handle SMS-based authentication using Redis for temporary code storage
    and an external SMS API for sending verification codes.
    """

    # Static configuration for SMS service
    sms_username = "9189629604"
    sms_apikey = "sf2xGcOmQvLuu5BkW5SCcOIrqJdzVKJIfdKMcscEhGrTyhWZ"
    sms_linenumber = "30007732903082"
    sms_text = "کاربر گرامی کد تأیید شما : "

    # Redis client for storing verification codes
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def __init__(self, phone_number):
        """
        Initialize the authenticator for a given phone number.
        A random verification code is generated.
        """
        self.phone_number = phone_number
        self.verify_code = 0

        # Store the generated code in Redis with expiration
        self.store_verification_code()

    def send_sms(self):
        """
        Sends the verification SMS to the user if not already sent.
        """
        # Check if a code is already stored for this phone number
        stored_code = Authenticator.redis_client.get(f'verification:{self.phone_number}')
        if stored_code:
            return {"status": "error", "message": "کاربر گرامی قبلاً برای شما کد ارسال شده است."}

        self.verify_code = random.randint(100000, 999999)

        # Prepare the SMS message
        message_text = Authenticator.sms_text + str(self.verify_code)

        # Configure the HTTP request for the SMS API
        conn = http.client.HTTPSConnection("api.sms.ir")
        request_url = (
            f"/v1/send?"
            f"username={quote(Authenticator.sms_username)}&password={quote(Authenticator.sms_apikey)}&"
            f"mobile={quote(self.phone_number)}&line={quote(Authenticator.sms_linenumber)}&"
            f"text={quote(message_text)}"
        )
        headers = {'Accept': 'text/plain'}

        try:
            # Send the HTTP GET request
            conn.request("GET", request_url, '', headers)
            response = conn.getresponse()
            response_data = response.read().decode("utf-8")

            # Handle the response
            if response.status == 200:
                self.store_verification_code()
                return {"status": "success", "message": "کد تأیید با موفقیت ارسال شد."}
            else:
                return {"status": "error", "message": f"کد تأیید ارسال نشد: {response_data}"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def verify_sms(self, entered_code):
        """
        Verifies the user-entered code against the stored code in Redis.
        """
        # Retrieve the stored code from Redis
        stored_code = Authenticator.redis_client.get(f'verification:{self.phone_number}')
        print(stored_code)
        print(entered_code)
        if not stored_code:
            return {"status": "error", "message": "کد شما نامعتبر است."}

        # Compare the entered code with the stored code
        if stored_code.decode() == entered_code:
            return {"status": "success", "message": "کد شما تأیید شد."}
        else:
            return {"status": "error", "message": "کد شما نا معتبر است..."}

    def store_verification_code(self):
        """
        Stores the verification code in Redis with a 20-second expiration.
        """
        Authenticator.redis_client.setex(f'verification:{self.phone_number}', 60, self.verify_code)

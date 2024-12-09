from flask import Flask, render_template, jsonify, request
from Authenticator import Authenticator

app = Flask(__name__)


@app.before_request
def before_request():
    """Hook to run before every request, if needed for initialization."""
    pass


@app.route('/')
def index():
    """Render the main index page."""
    return render_template("index.html")


@app.route('/send_code', methods=['POST'])
def send_code():
    """
    API endpoint to send a verification code to the provided phone number.
    Expects JSON payload:
    {
        "phone": "phone_number"
    }
    Returns:
        JSON response with success or error message.
    """
    data = request.get_json()
    phone_number = data.get('phone')

    if not phone_number:
        return jsonify({
            "status": "error",
            "message": "شماره تلفن معتبر ارسال نشده است."
        }), 400

    result = Authenticator.send_sms(phone_number)
    return jsonify(result)


@app.route('/verify_code', methods=['POST'])
def verify_code():
    """
    API endpoint to verify the code entered by the user.
    Expects JSON payload:
    {
        "phone": "phone_number",
        "code": "verification_code"
    }
    Returns:
        JSON response indicating whether the verification succeeded or failed.
    """
    data = request.get_json()
    phone_number = data.get('phone')
    entered_code = data.get('code')

    if not phone_number or not entered_code:
        return jsonify({
            "status": "error",
            "message": "شماره تلفن یا کد تأیید معتبر ارسال نشده است."
        }), 400

    result = Authenticator.verify_code(phone_number, entered_code)
    return jsonify(result)


@app.teardown_request
def teardown_request(exception=None):
    """
    Hook to clean up resources or handle request errors.
    Args:
        exception: The exception that occurred, if any.
    """
    if exception:
        app.logger.error(f"Error detected during request: {exception}")
    else:
        app.logger.info("Request completed successfully.")


if __name__ == "__main__":
    app.run(port=5001, debug=True)

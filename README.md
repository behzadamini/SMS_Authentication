
# Flask SMS Verification System

## Overview
This project is a simple Flask-based application for verifying users via SMS. It uses **Flask** for backend development, **Redis** for storing verification codes, and integrates with the **SMS.ir API** to send SMS codes. The frontend is powered by **Bootstrap** for styling and **Axios** for making HTTP requests.

---

## Features
- Send verification codes to users' phone numbers.
- Verify user-entered codes.
- Temporary storage of codes in Redis (with a 2-minute expiration).
- Error handling and input validation.
- Responsive frontend using Bootstrap.

---

## Technologies Used
### Backend
- **Flask**: For server-side logic.
- **Redis**: For storing and managing verification codes.
- **HTTP Client**: To connect with the SMS.ir API.

### Frontend
- **HTML/CSS**: For structuring and styling pages.
- **Bootstrap**: For responsive design.
- **Axios**: For making AJAX requests to the backend API.

---

## Prerequisites
Ensure the following are installed on your system:
- Python 3.8+ 
- Redis server

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/behzadamini/SMS_Authentication.git
   cd your-repository
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start Redis:
   Make sure Redis is running on your system. You can start it using:
   ```bash
   redis-server
   ```

5. Configure environment variables:
   Create a `.env` file in the root of your project and add the following:
   ```
   SMS_USERNAME=****
   SMS_APIKEY=****
   SMS_LINENUMBER=****
   ```

6. Run the Flask server:
   ```bash
   python app.py
   ```

7. Access the application:
   Open your browser and go to `http://localhost:5001`.

---

## Project Structure

```plaintext
project-root/
├── app.py                # Main Flask application
├── Authenticator.py      # SMS handling and Redis logic
├── templates/
│   └── index.html        # Frontend HTML template
├── static/
│   ├── css/              # Custom CSS files
│   ├── js/               # JavaScript files including Axios
│   └── bootstrap/        # Bootstrap assets
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## API Endpoints

### 1. Send Code
**URL**: `/send_code`  
**Method**: `POST`  
**Request Body**:
```json
{
  "phone": "user_phone_number"
}
```
**Response**:
- Success:
  ```json
  {
    "status": "success",
    "message": "کد تأیید با موفقیت ارسال شد."
  }
  ```
- Error:
  ```json
  {
    "status": "error",
    "message": "کاربر گرامی قبلاً برای شما کد ارسال شده است."
  }
  ```

---

### 2. Verify Code
**URL**: `/verify_code`  
**Method**: `POST`  
**Request Body**:
```json
{
  "phone": "user_phone_number",
  "code": "verification_code"
}
```
**Response**:
- Success:
  ```json
  {
    "status": "success",
    "message": "کد شما تأیید شد."
  }
  ```
- Error:
  ```json
  {
    "status": "error",
    "message": "کد شما نامعتبر است."
  }
  ```

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
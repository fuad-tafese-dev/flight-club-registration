from flask import Flask, request, render_template_string, redirect
import requests
import os

app = Flask(__name__)

# Configuration
SHEETY_ENDPOINT = "https://api.sheety.co/81a5e4dd4f52d720a6d48f81e653df05/userList/sheet1"
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

# Modern HTML template with CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flight Deal Club</title>
    <style>
        :root {
            --primary: #4361ee;
            --secondary: #3f37c9;
            --accent: #4895ef;
            --light: #f8f9fa;
            --dark: #212529;
            --success: #4cc9f0;
            --error: #f72585;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: #f5f7fa;
            color: var(--dark);
            line-height: 1.6;
        }

        .container {
            max-width: 600px;
            margin: 2rem auto;
            padding: 2rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: var(--primary);
            text-align: center;
            margin-bottom: 1.5rem;
        }

        .description {
            text-align: center;
            margin-bottom: 2rem;
            color: #6c757d;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }

        input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ced4da;
            border-radius: 5px;
            font-size: 1rem;
            transition: border-color 0.3s;
        }

        input:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(72, 149, 239, 0.25);
        }

        button {
            width: 100%;
            padding: 0.75rem;
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: var(--secondary);
        }

        .message {
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 5px;
            text-align: center;
        }

        .success {
            background-color: rgba(76, 201, 240, 0.2);
            color: #006d77;
        }

        .error {
            background-color: rgba(247, 37, 133, 0.2);
            color: #9d0208;
        }

        @media (max-width: 640px) {
            .container {
                margin: 1rem;
                padding: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>✈️ Join the Flight Deal Club</h1>
        <p class="description">
            Get exclusive access to the best flight deals directly to your inbox. 
            We'll notify you when prices drop to your favorite destinations!
        </p>

        <form method="post">
            <div class="form-group">
                <label for="first_name">First Name</label>
                <input type="text" id="first_name" name="first_name" required>
            </div>

            <div class="form-group">
                <label for="last_name">Last Name</label>
                <input type="text" id="last_name" name="last_name" required>
            </div>

            <div class="form-group">
                <label for="email1">Email</label>
                <input type="email" id="email1" name="email1" required>
            </div>

            <div class="form-group">
                <label for="email2">Confirm Email</label>
                <input type="email" id="email2" name="email2" required>
            </div>

            <button type="submit">Join the Club</button>
        </form>

        {% if message %}
            <div class="message {{ 'success' if 'in the club' in message else 'error' }}">
                {{ message }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        first = request.form["first_name"]
        last = request.form["last_name"]
        email1 = request.form["email1"]
        email2 = request.form["email2"]

        if email1 != email2:
            message = "Emails do not match. Please try again."
        else:
            data = {
                "sheet1": {
                    "firstName": first,
                    "lastName": last,
                    "email": email1
                }
            }
            headers = {
                "Authorization": f"Bearer {BEARER_TOKEN}",
                "Content-Type": "application/json"
            }

            response = requests.post(SHEETY_ENDPOINT, json=data, headers=headers)

            if response.status_code in (200, 201):
                message = "You're in the club! You'll start receiving flight deals soon."
            else:
                message = f"Registration failed. Error: {response.status_code} - {response.text}"

    return render_template_string(HTML_TEMPLATE, message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
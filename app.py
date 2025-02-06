from flask import Flask, request, jsonify
import requests
import math
import os

app = Flask(__name__)

def is_armstrong(num):
    """Checks if a number is an Armstrong number."""
    num_str = str(abs(int(num)))  # Convert to absolute integer string
    n = len(num_str)
    sum_of_powers = sum(int(digit) ** n for digit in num_str)
    return sum_of_powers == abs(num)

def get_number_properties(num):
    """Calculates mathematical properties of a number."""
    properties = []
    abs_num = abs(int(num))  # Convert to absolute value

    if is_armstrong(abs_num):  # Check Armstrong based on absolute value
        properties.append("armstrong")

    if int(num) % 2 != 0:
        properties.append("odd")
    else:
        properties.append("even")

    digit_sum = sum(int(digit) for digit in str(abs_num))  # Sum of digits

    return properties, digit_sum

def is_perfect(num):
    """Checks if a number is a perfect number."""
    if num <= 0:  # Prevent negative numbers from causing errors
        return False

    sum_of_divisors = sum(
        i + (num // i if i * i != num else 0)
        for i in range(1, int(math.sqrt(num)) + 1)
        if num % i == 0
    )

    return sum_of_divisors - num == num

def is_prime(num):
    """Checks if a number is prime."""
    if num <= 1:
        return False
    if num in (2, 3):
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

def get_fun_fact(num):
    """Fetches a fun fact about the number from Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{num}/math?json")
        response.raise_for_status()
        data = response.json()
        return str(data.get("text", "No fact available."))
    except requests.exceptions.RequestException:
        return "No fact available."

@app.route("/api/classify-number", methods=["GET"])
def classify_number():
    """API endpoint to classify a number."""
    number = request.args.get("number")

    if number is None:
        return jsonify({"error": True, "message": "Missing 'number' parameter"}), 400

    try:
        number = float(number) if "." in number else int(number)
    except ValueError:
        return jsonify({"number": number, "error": True, "message": "Invalid input"}), 400

    # Process the number's properties
    properties, digit_sum = get_number_properties(number)
    fun_fact = get_fun_fact(number)
    is_prime_val = is_prime(int(number))  # Prime check only for integers
    is_perfect_val = is_perfect(int(number))  # Perfect number check only for integers

    response_data = {
        "number": number,
        "is_prime": bool(is_prime_val),  # Ensure boolean format
        "is_perfect": bool(is_perfect_val),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

    return jsonify(response_data), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Railway's assigned PORT
    app.run(debug=False, host="0.0.0.0", port=port)
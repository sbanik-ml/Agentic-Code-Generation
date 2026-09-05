from flask import Flask, request, render_template_string, abort

app = Flask(__name__)

def is_prime(n: int) -> bool:
    """Return True if n is a prime number, False otherwise."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# HTML templates
FORM_HTML = """
<!doctype html>
<title>Prime Checker</title>
<h1>Prime Number Checker</h1>
<form method="post">
  <label for="number">Enter an integer:</label>
  <input type="text" id="number" name="number" required>
  <button type="submit">Check</button>
</form>
"""

RESULT_HTML = """
<!doctype html>
<title>Prime Checker Result</title>
<h1>Result</h1>
<p>The number <strong>{{ number }}</strong> is <strong>{{ result }}</strong>.</p>
<a href="{{ url_for('index') }}">Check another number</a>
"""

@app.route("/", methods=["GET"])
def index():
    """Render the input form."""
    return render_template_string(FORM_HTML)

@app.route("/", methods=["POST"])
def check_prime():
    """Process the submitted number and display whether it is prime."""
    raw = request.form.get("number", "").strip()
    try:
        num = int(raw)
    except ValueError:
        # Invalid input: not an integer
        abort(400, description="Invalid input: please provide an integer.")
    
    prime = is_prime(num)
    result_text = "a prime number" if prime else "not a prime number"
    return render_template_string(
        RESULT_HTML,
        number=num,
        result=result_text
    )

if __name__ == "__main__":
    # Run the Flask development server
    app.run(debug=True) 

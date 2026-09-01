"""Flask application entry point.

Provides a single route at ``/`` that renders ``index.html``.  On a POST
request the submitted number is validated and checked for primality using
the :func:`is_prime` function from the ``prime_checker`` module.
"""

from flask import Flask, render_template, request
from prime_checker import is_prime

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the home page and process prime‑checking submissions.

    Returns
    -------
    str
        Rendered HTML from ``templates/index.html``.
    """
    result = None
    error = None

    if request.method == "POST":
        # Expect a form field named ``number``.
        number_str = request.form.get("number", "").strip()
        if not number_str:
            error = "Please provide a number."
        else:
            try:
                number = int(number_str)
                # ``is_prime`` raises ``ValueError`` for non‑positive integers.
                result = is_prime(number)
            except ValueError as exc:
                error = str(exc)
            except Exception:
                error = "Invalid input. Ensure you entered an integer."

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    # Enable debug mode for development; remove or set to False in production.
    app.run(debug=True) 

from flask import Blueprint, render_template

# Create a Flask Blueprint named 'home_bp'
home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/')
def index():
	"""Home page route that renders home.html template."""
	return render_template('home.html')


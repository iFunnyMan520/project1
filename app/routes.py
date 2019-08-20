from flask import render_template
from app import app


@app.route('/')
def main_page():
	"""
	Draw main page with basic template
	"""
	return render_template('main_page.html')


@app.route('/api/user/login/')
def phone():
	return render_template('phone.html')


@app.route('/api/user/login/confirm/')
def confirm():
	return render_template('code.html')

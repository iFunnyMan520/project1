from flask import Flask, render_template
from app import app

@app.route('/api/user/login')
def phone():
	return render_template('phone.html')

@app.route('/api/user/login/confirm')
def confirm():
	return render_template('code.html')
from flask import Flask
from components.users import views


def bind(app: Flask):
	app.add_url_rule('/', view_func=views.MainPageView)
	app.add_url_rule(
		'/api/v1/user/login/',
		view_func=views.LoginView.as_view('login'))
	app.add_url_rule(
		'/api/v1/user/confirm/',
		view_func=views.ConfirmationView.as_view('confirmation'))
	app.add_url_rule(
		'/api/v1/users/me/',
		view_func=views.MeView.as_view('me'))
	app.add_url_rule(
		'/api/v1/users/logout/',
		view_func=views.LogoutView.as_view('logout'))

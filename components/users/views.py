from flask import request, Response, session, jsonify
from flask.views import MethodView

from components.users import utils
from components.users.models import User


class MainPageView(MethodView):

    def get(self):
        return b'Hello World'


class LoginView(MethodView):

    def post(self):
        if not request.json:
            return Response(status=400, response=b'Incoming data is not json')

        phone = request.json.get('phone')
        if not phone:
            return Response(status=400, response=b'Phone is not provided')

        confirmation_token = User.login(phone)
        utils.send_sms(confirmation_token.token)

        return Response(status=200, response=b'Sms was sent')


class ConfirmationView(MethodView):

    def post(self):
        if not request.json:
            return Response(status=400, response=b'Incoming data is not json')

        phone = request.json.get('phone')
        confirmation_token = request.json.get('token')

        if not phone or not confirmation_token:
            return Response(
                status=400, response=b'Phone or token was not provided')

        session_token, user = User.confirm_auth(phone, confirmation_token)

        if not session_token:
            return Response(
                status=400, response=b'Provided data was incorrect')

        session['session_token'] = session_token.session

        return jsonify(user.serialized)


class LogoutView(MethodView):
    def get(self):
        return Response(status=400, response=b'Does not working')


class MeView(MethodView):

    def get(self):
        session_token = session.get('session_token')

        if not session_token:
            return Response(status=403, response=b'Login in first')

        user = User.get_by_session(session_token)

        if not user:
            return Response(
                status=403, response=b'Session token was expired or invalid')

        return jsonify(user.serialized)

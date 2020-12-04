from flask import jsonify, g
from app import db
from ...auth import basic_auth
from ...blueprints.api import bp as api

@api.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db. session.commit()
    return jsonify({'token':token})


@api.route('/tokens', methods=['DELETE'])
@basic_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return jsonify({'message':'Success'}), 204
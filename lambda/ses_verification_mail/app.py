from chalice import Chalice
from chalicelib.verification import verification_email

app = Chalice(app_name='hackaton_ses_test')


@app.route('/')
def index():
    return 'Hello from the hackaton ses test'


@app.route("/send_verification_id", methods=["POST"])
def sent_verification_code():
    """Sent verification id to email"""
    body = app.current_request.json_body
    x = body.get('x', body)

    email = body.get('email', {})
    customer_id = body.get('customer_id', {})

    res = verification_email.send_verif_code(
        email=email,
        customer_id=customer_id
    )

    return res


@app.route("/confirm_verification_id", methods=["POST"])
def confirm_verification_code():
    """Confirm verification id to email"""
    body = app.current_request.json_body
    x = body.get('x', body)

    email = body.get('email', {})
    customer_id = body.get('customer_id', {})
    verification_code = body.get('verification_code', {})

    res = verification_email.confirmation_verif_code(
        customer_id=customer_id,
        verification_code = verification_code
    )

    return res

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

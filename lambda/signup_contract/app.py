from chalice import Chalice
from chalicelib.contract import save_contract_s3

app = Chalice(app_name='hackaton_contract_test')


@app.route('/')
def index():
    return 'Hello from the hackaton contract test'


@app.route("/write_contract", methods=["POST"])
def write_contract():
    """Write contract"""
    body = app.current_request.json_body
    x = body.get('x', body)

    customer_id = body.get('customer_id', {})

    res = save_contract_s3.write_html_contract_in_s3(customer_id=customer_id)

    return res
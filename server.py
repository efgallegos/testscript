from flask import Flask, jsonify, request
from flask import make_response
from config_entries import config_values
#from utilities.browser import getWebDriver, BrowserException
from batch_import import batch_import

def create_app():
    app = Flask(__name__)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)

    @app.route("/")
    def hello():
        return "Hello World!"

    @app.route('/igo', methods=['GET'])
    def list_api():
        result = {
            "igo/create":"Api used to create new cases with pre-filled data.",
            "igo/lock":"Api used to lock a existing case with pre-filled data."
        }
        return make_response(jsonify(result), 200)

    @app.route('/igo/create', methods=['GET'])
    def get_carriers():
        result = {
            "carriers": config_values["carriers"],
        }
        return make_response(jsonify(result), 200)

    @app.route('/igo/create/<name>', methods=['GET'])
    def get_product(name):
        if name in config_values["carriers"]:
            result = {
                "carrier": name,
                "products": config_values[name]["products"],
            }
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify({"products": 'Not Found'}), 404)

    @app.route('/igo/create/<name>/<product>', methods=['GET'])
    def get_states(name, product):
        if name in config_values["carriers"] and product in config_values[name]['products']:
            result = {
                "carrier": name,
                "product": product,
                "states": config_values[name][product]['states'],
            }
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify({"states": 'Not Found'}), 404)

    @app.route('/igo/create/<name>/<product>/<state>', methods=['GET'])
    def get_plans(name, product,state):
        if (name in config_values["carriers"] and
            product in config_values[name]['products'] and
            state in config_values[name][product]['states']):
            result = {
                "carrier": name,
                "product": product,
                "state": state,
                "plans": config_values[name][product]['plans'],
            }
            return make_response(jsonify(result), 200)
        else:
            return make_response(jsonify({"plans": 'Not Found'}), 404)

    @app.route('/igo/create/<name>/<product>/<state>/<plan>', methods=['GET'])
    def create_case(name, product, state, plan):
        b = request.args.get('browser', 'Firefox')
        e = request.args.get('env', 'qd3')
        u = request.args.get('usr', 'tombqd5')
        p = request.args.get('pass', 'password1')

        try:
            result = {}
            result['browser'] = name
            result['product'] = product
            result['state']  = state
            result['plan'] = plan
            ##################################################
            #####    Call to iGo batch import case       #####
            ##################################################
            batch_import([b,name,e,u,p,product,state,plan])
            result['status'] = "Case was created successfully."
            return make_response(jsonify(result), 200)

        except Exception as e:
            result = {}
            result['browser'] = name
            result['product'] = product
            result['state']  = state
            result['plan'] = plan
            result['status'] = "Case creation failed."
            result['error msg'] = str(e)
            return make_response(jsonify(result), 404)
        #finally:
        #    driver.quit()
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8081)

#!flask/bin/python
from flask import Flask, jsonify, abort
from flask import request
from boto.sqs.message import Message
import boto.sqs

app = Flask(__name__)

conn = boto.sqs.connect_to_region("us-west-2")
q = conn.get_queue("toli-q-1")

@app.route('/metrics/v1.0/generate', methods=['POST'])
# expecting JSON to come with {type, message, client_data} strings
def create_event():
    if not request.json or not 'type' in request.json:
        print "no TYPE in object"
        abort(400)

    m = Message()
    the_type = request.json['type']
    m.set_body("type =>" + the_type)
    m.message_attributes = {
         "type": {
             "data_type": "String",
             "string_value": the_type
         },
         "message": {
             "data_type": "String",
             "string_value": request.json['message']
         },
         "client_data": {
             "data_type": "String",
             "string_value": request.json['client_data']
         }
     }
    print "created a message " + str(m) + " for [" + the_type + "]"
    print "sending it on connection: " + str(conn)
    q.write(m)
    return jsonify({'generated event': m.get_body()}), 201

if __name__ == '__main__':
    app.run(debug=True)

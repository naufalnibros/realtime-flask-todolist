from flask import Flask, render_template, request, jsonify
from pusher import Pusher
import json

# create flask app
app = Flask(__name__)

# Config pusher object
pusher = Pusher(
  app_id='652743',
  key='9e69cf938bf35bf84c6a',
  secret='41a17b5f6291483c0d45',
  cluster='ap1',
  ssl=True
)

# index route, shows index.html view
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint for stopping todo item
@app.route('/add-todo', methods=['POST'])
def addTodo():
    data = json.loads(request.data) # load JSON data from request
    pusher.trigger('flask-pusher', 'item-added', data) # trigger `item-added` event on `todo` channel
    return jsonify(data)

# Endpoint for deleting todo item
@app.route('/remove-todo/<item_id>')
def removeTodo(item_id):
    data = {'id': item_id}
    pusher.trigger('flask-pusher', 'item-removed', data)
    return jsonify(data)

# Endpoint for updating todo item
@app.route('/update-todo/<item_id>', methods=['POST'])
def updateTodo(item_id):
    data = {
        'id'        : item_id,
        'complete'  : json.loads(request.data).get('completed', 0)
    }
    pusher.trigger('flask-pusher', 'item-update', data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

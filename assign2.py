# Importing libraries
from transformers.pipelines import pipeline
from flask import Flask,request,jsonify
import time

# Create flask app
# Try to handle a error model also
app = Flask(__name__)

# Define a handler for / path
@app.route("/")
def hello_world():
    return "<p>Hello,world</p>"

models_list = []

@app.route("/models", methods =['GET'])
def modelslist_output():
    global models_list
    # Returning the dictionary as response
    return jsonify(models_list)

@app.route("/models", methods =['PUT'])
def models_input():
    data = request.json
    global models_list
    output = {
        "name": data['name'],
        "tokenizer": data['tokenizer'],
        "model": data['model']
    }
    models_list.append(output)

    # Returning the dictionary as response
    return jsonify(models_list)

@app.route("/models", methods =['DELETE'])
def models_delete():
    global models_list
    model_name = request.args.get('model')
    newlist_models = [i for i in models_list if not (i['model'] == model_name)]
    models_list = newlist_models
    # Returning the dictionary as response
    return jsonify(models_list)

# Define a handler for /answer path which processes a json payload with question and context and return an answer
@app.route("/answer", methods =['POST'])
def answer():
    global models_list
    model_name = request.args.get('model')
    data = request.json
    required_model = [i for i in models_list if (i['model'] == model_name)]
    if len(required_model) ==0:
        return print("The selected model is not a part of the model list in API")
    # Importing the model for question answering
    # Could be improved by not importing the model
    hg_comp = pipeline('question-answering', model=required_model[0]['model'],
                       tokenizer=required_model[0]['tokenizer'])
    answer = hg_comp({'question': data['question'], 'context': data['context']})['answer']

    # Create the response body
    output = {
        "timestamp": int(time.time()),
        "model": model_name,
        "answer": answer,
        "question": data['question'],
        "context": data['context']
    }
    return jsonify(output)

# Run if running "pyhton answer.py"
if __name__=='__main__':
    # For Running API
    app.run(host='0.0.0.0',port=8000, threaded=True)






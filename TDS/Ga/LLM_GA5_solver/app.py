from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate_question', methods=['POST'])
def evaluate_question():
    question = request.form.get('question')
    api_token = request.form.get('api_token')

    # Fetch the models list from the API
    response = requests.get(
        'https://aiproxy.sanand.workers.dev/openai/v1/models',
        headers={'Authorization': f'Bearer {api_token}'}
    )

    if response.status_code != 200:
        return jsonify({"points": 0, "error": "Failed to fetch models: " + response.text}), response.status_code

    models = response.json()

    # Sort models by created date (most recent first)
    sorted_models = sorted(models['data'], key=lambda x: x['created'], reverse=True)

    points = 0

    # Debugging
    print("Sorted Models:")
    for i, model in enumerate(sorted_models):
        print(f"{i}: {model['id']} - {model['created']}")

    # First question evaluation
    gpt_3_5_turbo_0301 = next((model for model in sorted_models if model['id'] == "gpt-3.5-turbo-0301"), None)
    if gpt_3_5_turbo_0301 and gpt_3_5_turbo_0301['created'] == "2023-03-06":
        points += 4
    print(f"GPT-3.5-turbo-0301 check: {points} points")

    # Second question evaluation
    if len(sorted_models) > 22 and sorted_models[22]['id'] == "davinci-002":
        points += 2
    print(f"Davinci-002 index check: {points} points")

    # Third question evaluation
    gpt4_turbo_index = next((i for i, model in enumerate(sorted_models) if model['id'] == "gpt-4-turbo-2024-04-09"), None)
    gpt3_5_turbo_instruct_index = next((i for i, model in enumerate(sorted_models) if model['id'] == "gpt-3.5-turbo-instruct"), None)
    if gpt4_turbo_index is not None and gpt3_5_turbo_instruct_index is not None and gpt4_turbo_index + 17 == gpt3_5_turbo_instruct_index:
        points += 1
    print(f"GPT-4-turbo and GPT-3.5-turbo-instruct check: {points} points")

    return jsonify({"points": points})

if __name__ == '__main__':
    app.run(debug=True)

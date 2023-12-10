import requests
import json
from termcolor import colored

def send_to_model(user_input):
    data = {
        "messages": [
            {"role": "system", "content": "You're a helpful bot"},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 150,
        "stream": True
    }
    
    server_url = 'http://localhost:1234/v1/chat/completions'
    
    with requests.post(server_url, json=data, stream=True) as response:
        if response.encoding is None:
            response.encoding = 'utf-8'

        print(colored("Bot: ", "blue"), end='', flush=True)
        for line in response.iter_lines(decode_unicode=True):
            if line.startswith('data:'):  # Check if the line starts with 'data:'
                try:
                    json_response = json.loads(line[len('data: '):])  # Parse the JSON after 'data: '
                    model_response = json_response.get('choices')[0].get('delta').get('content')
                    if model_response:  # Check if model_response is not None
                        print(model_response, end='', flush=True)  # Print each token as it is received
                except json.JSONDecodeError:
                    pass  # Ignore JSON parsing errors and continue
        
        print()
        
def main():
    print("Talk to the model. Type 'quit' to exit.")
    
    while True:
        user_input = input(colored("You: ", "yellow"))
        if user_input.lower() == 'quit':
            break
        send_to_model(user_input)

if __name__ == '__main__':
    main()

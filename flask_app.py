from flask import Flask, request, jsonify
import json
from read_pickle import retrieve_top_documents
import pickle

app = Flask(__name__)

start_domain = 'iit.edu' ### change to reference the start_domain attribute in crawler

### this function validates the passed data to ensure it matches
### expected format for this query processor
#### json queries must be
### {"Query": str(user query), "K": int(top k results)}
def validate_json(data):
    try:
        parsed_data = json.loads(data)

        ### ensure Query field is present and the associated data is a string
        if 'Query' not in parsed_data or not isinstance(parsed_data['Query'], str):
            return "Query Error"

        #### ensure K field is present (top k results) and that it is an integer
        if 'K' not in parsed_data or not isinstance(parsed_data['K'], int):
            return "K error"

        return 'Valid'

    ### if cannot parse given data as JSON - return flag 'not JSON'
    except json.JSONDecodeError:
        return 'Not JSON'

@app.route('/make-query', methods=['POST'])
def process_data():
    # ensure request is json
    if request.is_json:
        # Validate JSON payload
        validation_message = validate_json(request.get_data())
        if validation_message == 'Valid':
            data = request.get_json()

            # Extract 'Query' and 'K' from JSON payload
            query = data['Query'].lower()
            k = data['K']

            try:
                ## reads in inverted index generated by inverted_index_generator
                try:
                    inverted_index = load_inverted_index_from_pickle(f'{start_domain}_inverted_index.pkl')
                except Exception as e:
                    return f'Inverted index .pkl file {f'{start_domain}_inverted_index.pkl'} not found.', 500

                # Call retrieve_top_documents function from read_pickle.py
                results = retrieve_top_documents(query, inverted_index, k)

                response_message = f"\nQuery: \"{query}\" top {k} result(s)\n\n"
                for rank, (doc_id, relevance_score) in enumerate(results, start=1):
                    response_message += f"Rank {rank}: Document ID {doc_id}\n" #(Relevance Score: {relevance_score})\n"

                # Return the response message as plain text
                return response_message, 200, {'Content-Type': 'text/plain'}
            except Exception as e:
                return f'Inverted index .pkl file {f'{start_domain}_inverted_index.pkl'} not found.', 500
            # Process the data (perform desired operations with query and k)

            return jsonify(response_data), 200

        elif validation_message == "Not JSON":
            return 'Invalid JSON format', 400, {'Content-Type': 'text/plain'}

        elif validation_message == "Query Error":
            return 'Query Error: Include a \'Query\' in the JSON request of Type Str', 400, {'Content-Type': 'text/plain'}

        elif validation_message == "K error":
            return 'Top K Error: Include a \'K\' in the JSON of Type Int for top k results', 400, {'Content-Type': 'text/plain'}
        else:
            return 'Error: Invalid JSON format or missing required fields', 400, {'Content-Type': 'text/plain'}

    ## else for request not json
    else:
        return f'Request is not in valid JSON format', 400, {'Content-Type': 'text/plain'}

def load_inverted_index_from_pickle(pickle_file):
    try:
        with open(pickle_file, 'rb') as f:
            inverted_index = pickle.load(f)
        return inverted_index
    except FileNotFoundError:
        return f"Error: File '{pickle_file}' not found.", 400, {'Content-Type': 'text/plain'}

        return None
    except Exception as e:
        return f'Error occurred while loading pickle file: {str(e)}', 400, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)




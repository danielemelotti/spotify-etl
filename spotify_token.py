import requests

# Exchange the authorization code for an access token
def exchange_code_for_token(authorization_code):
    client_id = 'YOUR CLIENT ID' # SENSITITVE 
    client_secret = 'YOUR CLIENT SECRET' # SENSITITVE 
    redirect_uri = 'http://localhost:8888/callback'
    code = authorization_code

    # Prepare the data for the POST request
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }

    # Make the POST request to get the access token
    response = requests.post('https://accounts.spotify.com/api/token', data=payload)
    return response.json()  # This contains the access token and other info

# Example usage:
token_info = exchange_code_for_token('YOUR AUTH CODE') # SENSITITVE 
print(token_info)

import urllib.parse

# Generate an authentication code
def generate_auth_url():
    client_id = 'YOUR CLIENT ID'  #SENSITIVE
    redirect_uri = 'http://localhost:8888/callback'  
    scope = 'user-read-recently-played'
    
    # Encode the parameters
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope
    }
    query_string = urllib.parse.urlencode(params)
    
    auth_url = f"https://accounts.spotify.com/authorize?{query_string}"
    return auth_url

print("Follow this URL to authorize your application:")
print(generate_auth_url())

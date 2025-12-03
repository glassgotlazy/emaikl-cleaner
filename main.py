from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/get-spam', methods=['POST'])
def get_spam():
    data = request.json
    access_token = data.get('access_token')
    max_results = data.get('max_results', 50)
    
    try:
        creds = Credentials(token=access_token)
        service = build('gmail', 'v1', credentials=creds)
        
        results = service.users().messages().list(
            userId='me',
            q='is:spam',
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        emails = []
        
        for msg in messages:
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
            
            emails.append({
                'id': msg['id'],
                'subject': subject,
                'sender': sender,
                'date': date,
                'preview': message.get('snippet', '')
            })
        
        return jsonify({'emails': emails})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-email', methods=['POST'])
def delete_email():
    data = request.json
    access_token = data.get('access_token')
    email_id = data.get('email_id')
    
    try:
        creds = Credentials(token=access_token)
        service = build('gmail', 'v1', credentials=creds)
        service.users().messages().trash(userId='me', id=email_id).execute()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#!/usr/bin/env python3
import json
import html
from datetime import datetime

def load_chat_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def format_timestamp(timestamp):
    dt = datetime.fromisoformat(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def get_user_color(username):
    colors = {
        'Worker-Sirius': '#3498db',
        'Supervisor-Andromeda': '#e74c3c',
    }
    return colors.get(username, '#7f8c8d')

def escape_text(text):
    text = html.escape(text)
    text = text.replace('\\!', '!')
    text = text.replace('\\n', '<br>')
    return text

def generate_html(chat_data):
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat History</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        
        .chat-container {
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 30px;
        }
        
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        
        .message {
            margin-bottom: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            background-color: #f8f9fa;
            border-left: 4px solid;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .message:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .message-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .username {
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .timestamp {
            color: #6c757d;
            font-size: 0.9em;
        }
        
        .message-text {
            color: #495057;
            line-height: 1.8;
        }
        
        .stats {
            margin-top: 30px;
            padding: 20px;
            background-color: #e9ecef;
            border-radius: 8px;
            text-align: center;
        }
        
        .stats h2 {
            color: #495057;
            margin-bottom: 15px;
        }
        
        .stat-item {
            display: inline-block;
            margin: 0 20px;
            padding: 10px 20px;
            background-color: white;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .stat-label {
            color: #6c757d;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>Chat History</h1>
'''
    
    for message in chat_data['messages']:
        username = message['from']
        timestamp = format_timestamp(message['time'])
        text = escape_text(message['text'])
        color = get_user_color(username)
        
        html_content += f'''
        <div class="message" style="border-left-color: {color};">
            <div class="message-header">
                <span class="username" style="color: {color};">{username}</span>
                <span class="timestamp">{timestamp}</span>
            </div>
            <div class="message-text">{text}</div>
        </div>
'''
    
    total_messages = len(chat_data['messages'])
    users = list(set(msg['from'] for msg in chat_data['messages']))
    
    html_content += f'''
        <div class="stats">
            <h2>Chat Statistics</h2>
            <div class="stat-item">
                <div class="stat-value">{total_messages}</div>
                <div class="stat-label">Total Messages</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{len(users)}</div>
                <div class="stat-label">Participants</div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    return html_content

def main():
    chat_data = load_chat_data('chat.json')
    html_content = generate_html(chat_data)
    
    with open('chat.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Successfully converted chat.json to chat.html")
    print(f"📊 Processed {len(chat_data['messages'])} messages")

if __name__ == '__main__':
    main()
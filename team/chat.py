#!/usr/bin/env python3
import json
import sys
from datetime import datetime

CHAT_FILE = "chat.json"

def send(agent_id, message):
    """Send a message to the chat room"""
    try:
        with open(CHAT_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"messages": [], "last_read": {}}
    
    # Check if agent has unread messages
    last_read_index = data.get("last_read", {}).get(agent_id, -1)
    total_messages = len(data["messages"])
    
    if last_read_index < total_messages - 1:
        print(f"Error: You have {total_messages - last_read_index - 1} unread messages. Please check first.")
        return
    
    data["messages"].append({
        "time": datetime.now().isoformat(),
        "from": agent_id,
        "text": message
    })
    
    with open(CHAT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print("Message sent")

def check(agent_id):
    """Check for new messages since this agent's last read"""
    try:
        with open(CHAT_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No messages yet")
        return
    
    last_read_index = data.get("last_read", {}).get(agent_id, -1)
    new_messages = data["messages"][last_read_index + 1:]
    
    if new_messages:
        for msg in new_messages:
            if msg["from"] != agent_id:  # Don't show own messages
                print(f"[{msg['time']}] {msg['from']}: {msg['text']}")
        
        # Update last read position
        data["last_read"][agent_id] = len(data["messages"]) - 1
        with open(CHAT_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    else:
        print("No new messages")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python chat.py <agent_id> send <message>")
        print("       python chat.py <agent_id> check")
        sys.exit(1)
    
    agent_id = sys.argv[1]
    action = sys.argv[2]
    
    if action == "send" and len(sys.argv) > 3:
        message = " ".join(sys.argv[3:])
        send(agent_id, message)
    elif action == "check":
        check(agent_id)
    else:
        print("Invalid command")
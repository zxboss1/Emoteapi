
import asyncio
import threading
import os
from flask import Flask, request, jsonify
from bot_module import client, command_queue, start_bot

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Free Fire Emote Bot API",
        "bot_ready": client.bot_ready,
        "timing_info": {
            "join_wait": "0.4 seconds",
            "emote_delay": "Simultaneous for all UIDs",
            "leave_wait": "0.1 seconds",
            "total_approx": "~0.5 seconds for any number of UIDs"
        },
        "endpoints": {
            "join": "/join?tc=TEAMCODE&uid1=UID1&uid2=UID2&uid3=UID3&uid4=UID4&uid5=UID5&emote_id=EMOTE_ID",
            "status": "/status"
        }
    })

@app.route('/join')
def join_and_emote():
    """Join team and perform emotes"""
    try:
        team_code = request.args.get('tc')
        emote_id = request.args.get('emote_id', '909000001')
        
        # Collect all UIDs
        uids = []
        for i in range(1, 6):
            uid = request.args.get(f'uid{i}')
            if uid:
                try:
                    uids.append(int(uid))
                except ValueError:
                    pass
        
        if not team_code:
            return jsonify({
                "status": "error",
                "message": "Team code (tc) is required"
            }), 400
        
        if not uids:
            return jsonify({
                "status": "error",
                "message": "At least one UID is required (uid1, uid2, etc.)"
            }), 400
        
        if not client.bot_ready:
            return jsonify({
                "status": "error",
                "message": "Bot is not ready yet. Please wait."
            }), 503
        
        # Add command to queue
        command_queue.put({
            'type': 'join_and_emote',
            'team_code': team_code,
            'uids': uids,
            'emote_id': int(emote_id)
        })
        
        return jsonify({
            "status": "success",
            "message": "Command queued successfully",
            "data": {
                "team_code": team_code,
                "uids": uids,
                "emote_id": emote_id,
                "estimated_time": "~0.5 seconds"
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/status')
def status():
    """Check bot status"""
    return jsonify({
        "status": "online" if client.bot_ready else "starting",
        "bot_ready": client.bot_ready,
        "connections": {
            "online": client.online_writer is not None,
            "chat": client.whisper_writer is not None
        },
        "timing_optimized": True
    })

def run():
    """Start the bot and Flask app"""
    # Start bot in background thread
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    # Start Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    run()

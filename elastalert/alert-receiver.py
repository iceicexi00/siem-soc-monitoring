#!/usr/bin/env python3
from flask import Flask, request
import json, datetime

app = Flask(__name__)
LOG_FILE = '/var/log/siem-alerts.jsonl'

@app.route('/alert', methods=['POST'])
def alert():
    try:
        data = request.get_json(force=True)
    except Exception:
        data = {'raw': request.data.decode('utf-8', errors='replace')}

    record = {
        'received_at': datetime.datetime.now().isoformat(),
        'remote_addr': request.remote_addr,
        'payload': data,
    }

    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"[ALERT] {record['received_at']}: {json.dumps(data, ensure_ascii=False)[:300]}", flush=True)
    return 'OK', 200

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

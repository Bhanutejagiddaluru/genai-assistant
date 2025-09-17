import argparse, requests
ap = argparse.ArgumentParser(); ap.add_argument("--q", required=True); ap.add_argument("--index", default="./data/index")
args = ap.parse_args()
r = requests.post("http://localhost:8000/chat", json={"question":args.q,"index_dir":args.index})
print(r.json())

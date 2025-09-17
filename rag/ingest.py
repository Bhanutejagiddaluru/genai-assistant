import argparse, pathlib
from .retriever import build_index

def build_or_update_index(docs_dir, index_dir, rebuild=True):
    p = pathlib.Path(index_dir)
    if rebuild and p.exists():
        for f in p.glob("*"): f.unlink()
    return build_index(docs_dir, index_dir)

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="./data/docs")
    ap.add_argument("--index", default="./data/index")
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()
    print(build_or_update_index(args.docs, args.index, args.rebuild))

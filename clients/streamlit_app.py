import os, json, asyncio, websockets, requests, streamlit as st
API_URL = os.getenv("API_URL","http://localhost:8000")
st.title("GenAI Assistant")
docs_dir = "./data/docs"; index_dir="./data/index"
if st.button("Ingest"):
    r = requests.post(f"{API_URL}/ingest", json={"docs_dir":docs_dir,"index_dir":index_dir,"rebuild":True})
    st.write(r.json())
q = st.text_input("Ask a question:")
if st.button("Ask"):
    async def stream_answer():
        uri = API_URL.replace("http","ws")+"/ws/stream"
        async with websockets.connect(uri) as ws:
            await ws.send(json.dumps({"question":q,"index_dir":index_dir}))
            buf=""
            while True:
                chunk = await ws.recv()
                if chunk=="[[END]]": break
                buf+=chunk; st.markdown(buf)
    asyncio.run(stream_answer())

import streamlit as st
from collections import deque
import hashlib

# ---- deterministic fake links -----
def generate_links(url, max_links=3):
    h = hashlib.md5(url.encode()).hexdigest()
    nums = [int(h[i:i+2], 16) for i in range(0, len(h), 2)]
    neighbors = []
    domain = url.split('//')[-1].split('/')[0]
    for i in range(max_links):
        idx = nums[i] % 5 + 1
        if nums[i+5] % 4 == 0:
            neighbors.append(f"https://{domain}/page{idx}")
        elif nums[i+5] % 4 == 1:
            neighbors.append(f"https://{domain}/post{idx}")
        else:
            neighbors.append(f"https://site{(nums[i+7]%10)}.org/article{idx}")
    return list(dict.fromkeys(neighbors))

# ---- crawler -----
def crawler(start_url, mode, max_depth):
    visited = set([start_url])
    depth = {start_url: 0}
    queue = deque([start_url]) if mode=="BFS" else [start_url]
    result = []

    while queue:
        node = queue.popleft() if mode=="BFS" else queue.pop()
        d = depth[node]
        neighbors = generate_links(node)
        result.append((node, d, neighbors))
        if d < max_depth:
            for nb in neighbors:
                if nb not in visited:
                    visited.add(nb); depth[nb]=d+1
                    queue.append(nb)
    return result

# ---- UI -----
st.set_page_config(page_title="Web Crawler", page_icon="🌐", layout="wide")

with open("styles.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 class='title'>🌐 Glass Web Crawler Simulator</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([3,1,1])
with col1:
    start = st.text_input("Start URL:", "https://example.com")
with col2:
    mode = st.selectbox("Mode:", ["BFS","DFS"])
with col3:
    depth = st.slider("Max Depth", 0, 6, 3)

if st.button("🚀 Start Crawl"):
    results = crawler(start, mode, depth)
    for url, d, links in results:
        with st.expander(f"📍 {url} — Depth {d}"):
            st.write("### Discovered Links:")
            for l in links:
                st.markdown(f"- {l}")
    st.success("✅ Crawl Complete")
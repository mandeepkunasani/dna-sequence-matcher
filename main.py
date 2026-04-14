import streamlit as st
import time

st.set_page_config(page_title="DNA Matcher", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#020617,#022c22);
    color:#86efac;
}
.title {
    font-size:35px;
    font-weight:bold;
    color:#22c55e;
}
.highlight {
    background:#facc15;
    color:black;
    padding:3px;
    border-radius:5px;
}
.stButton>button {
    background:#22c55e;
    color:black;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🧬 DNA Sequence Matcher (Rabin-Karp)</div>', unsafe_allow_html=True)

# ---------- INPUT ----------
dna = st.text_area("Enter DNA Sequence (A, T, G, C)", "ATGCGATACGCTTGCAT")
pattern = st.text_input("Enter Gene Pattern", "TGC")

run = st.button("🔍 Find Pattern")

# ---------- RABIN-KARP ----------
def rabin_karp(text, pattern):
    d = 256
    q = 101
    m = len(pattern)
    n = len(text)

    h = pow(d, m-1) % q
    p = 0
    t = 0

    matches = []

    for i in range(m):
        p = (d*p + ord(pattern[i])) % q
        t = (d*t + ord(text[i])) % q

    for i in range(n-m+1):
        yield i, p, t

        if p == t:
            if text[i:i+m] == pattern:
                matches.append(i)

        if i < n-m:
            t = (d*(t - ord(text[i])*h) + ord(text[i+m])) % q
            if t < 0:
                t += q

# ---------- RUN ----------
if run:
    st.subheader("🧠 Matching Process")

    placeholder = st.empty()
    found_positions = []

    for i, ph, th in rabin_karp(dna, pattern):
        highlighted = dna[:i] + f"<span class='highlight'>{dna[i:i+len(pattern)]}</span>" + dna[i+len(pattern):]
        placeholder.markdown(highlighted, unsafe_allow_html=True)

        st.write(f"Index: {i} | Pattern Hash: {ph} | Window Hash: {th}")

        if dna[i:i+len(pattern)] == pattern:
            found_positions.append(i)

        time.sleep(0.3)

    st.success("Search Completed ✅")

    if found_positions:
        st.write(f"🔬 Matches Found at positions: {found_positions}")
    else:
        st.error("No Match Found ❌")

# ---------- MUTATION MODE ----------
st.subheader("🧪 Mutation Test")

mut = st.text_input("Enter Mutated DNA", "")

if st.button("Test Mutation"):
    if pattern in mut:
        st.success("Pattern still exists ✅")
    else:
        st.warning("Pattern lost due to mutation ❌")
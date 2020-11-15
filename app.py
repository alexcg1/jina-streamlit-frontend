import streamlit as st
from util import get_results, render_results, Getter, Defaults, Renderer, Encoder


st.title("Jina Search")
media_option = ["Text", "Image"]

st.sidebar.title("Options")
media_select = st.sidebar.selectbox(label="Media", options=media_option)
endpoint = st.sidebar.text_input("Endpoint", value=Defaults.endpoint)
if media_select == "Text":
    query = st.text_input(
        "What do you wish to search?", value=Defaults.text_query
    )
elif media_select == "Image":
    query = st.file_uploader("File")
    if query:
        encoded_query = Encoder.img_base64(query.read())

top_k = st.sidebar.slider("Top K", min_value=1, max_value=20, value=10)

if st.button("Search"):
    if media_select == "Text":
        results = get_results(query=query, top_k=top_k)
        st.markdown(render_results(results))
    elif media_select == "Image":
        results = Getter.images(endpoint=endpoint, query=encoded_query, top_k=top_k)  # Just uses hardcoded image for now
        html = Renderer.images(results)
        st.write(html, unsafe_allow_html=True)
    st.balloons()

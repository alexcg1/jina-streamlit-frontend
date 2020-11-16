import streamlit as st
from PIL import Image
from util import get_results, render_results, Getter, Defaults, Renderer, Encoder
from streamlit_drawable_canvas import st_canvas


st.title("Jina Search")
media_option = ["Text", "Image", "Draw"]

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
elif media_select == "Draw":
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    bg_color = st.sidebar.color_picker("Background color hex: ", "#ffffff")
    bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
    drawing_mode = st.sidebar.selectbox(
        "Drawing tool:", ("freedraw", "line", "rect", "circle", "transform")
    )
    realtime_update = st.sidebar.checkbox("Update in realtime", True)

    data = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="" if bg_image else bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        width=400,
        height=400,
        drawing_mode=drawing_mode,
        key="canvas",
    )

    # Do something interesting with the image data and paths
    import base64
    from io import BytesIO
    if data is not None:
        if data.image_data is not None:
            img_data = data.image_data
            # if st.button("Save image as base64"):
                # im = Image.fromarray(img_data.astype('uint8'), mode="RGBA")
                # buffered = BytesIO()
                # im.save(buffered, format="PNG")
                # img_str = base64.b64encode(buffered.getvalue())
                # st.write(img_str)

            im = Image.fromarray(img_data.astype('uint8'), mode="RGBA")
            buffered = BytesIO()
            im.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue())
            output = str(img_str)[2:-1]
            encoded_query = f'["data:image/png;base64,{output}"]'
            # st.write(encoded_query)


        # from pprint import pprint
        # img = data.image_data
        # st.image(img)
        # st.write(dir(img))
        # st.write(img)
        # st.write(type(img))
        # if st.button("Convert"):
            # output = Encoder.ndarray_to_png(img)
            # output = Encoder.rgb_ndarray_to_png(img)
            # st.write(type(output))




top_k = st.sidebar.slider("Top K", min_value=1, max_value=20, value=10)

if st.button("Search"):
    if media_select == "Text":
        results = get_results(query=query, top_k=top_k)
        st.markdown(render_results(results))
    elif media_select == "Image" or media_select == "Draw":
        results = Getter.images(endpoint=endpoint, query=encoded_query, top_k=top_k)  # Just uses hardcoded image for now
        html = Renderer.images(results)
        st.write(html, unsafe_allow_html=True)
    st.balloons()

import requests

default_phrase = "hey, dude"
default_top_k = 10
endpoint = "http://0.0.0.0:45678/api/search"


def get_image_results(
    query: str = "", top_k: int = default_top_k, endpoint=endpoint
) -> list:
    from pprint import pprint
    import sys

    headers = {
        "Content-Type": "application/json",
    }

    data = f'{{"top_k": {top_k}, "mode": "search", "data": ["text:{query}"]}}'

    response = requests.post(endpoint, headers=headers, data=data)

    content = response.json()
    return content
    sys.exit()
    results = []
    results_raw = content["search"]["docs"][0]["topkResults"]
    for result in results_raw:
        text = result["matchDoc"]["text"]
        results.append(text)

    return results


def get_results(query: str = "", top_k: int = default_top_k) -> list:
    headers = {
        "Content-Type": "application/json",
    }

    data = f'{{"top_k": {top_k}, "mode": "search", "data": ["text:{query}"]}}'

    response = requests.post(endpoint, headers=headers, data=data)

    content = response.json()
    results = []
    results_raw = content["search"]["docs"][0]["topkResults"]
    for result in results_raw:
        text = result["matchDoc"]["text"]
        results.append(text)

    return results


def render_results(results: list) -> str:
    header = """
    | Name | Line |
    | ---  | ---  |
    """
    output = header
    for text in results:
        character, words = text.split("[SEP]")
        result_text = f"| **{character}** | {words} |\n"
        output += result_text

    return output


default_img = '["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAIAAABLbSncAAAA2ElEQVR4nADIADf/AxWcWRUeCEeBO68T3u1qLWarHqMaxDnxhAEaLh0Ssu6ZGfnKcjP4CeDLoJok3o4aOPYAJocsjktZfo4Z7Q/WR1UTgppAAdguAhR+AUm9AnqRH2jgdBZ0R+kKxAFoAME32BL7fwQbcLzhw+dXMmY9BS9K8EarXyWLH8VYK1MACkxlLTY4Eh69XfjpROqjE7P0AeBx6DGmA8/lRRlTCmPkL196pC0aWBkVs2wyjqb/LABVYL8Xgeomjl3VtEMxAeaUrGvnIawVh/oBAAD///GwU6v3yCoVAAAAAElFTkSuQmCC", "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAIAAABLbSncAAAA2ElEQVR4nADIADf/AvdGjTZeOlQq07xSYPgJjlWRwfWEBx2+CgAVrPrP+O5ghhOa+a0cocoWnaMJFAsBuCQCgiJOKDBcIQTiLieOrPD/cp/6iZ/Iu4HqAh5dGzggIQVJI3WqTxwVTDjs5XJOy38AlgHoaKgY+xJEXeFTyR7FOfF7JNWjs3b8evQE6B2dTDvQZx3n3Rz6rgOtVlaZRLvR9geCAxuY3G+0mepEAhrTISES3bwPWYYi48OUrQOc//IaJeij9xZGGmDIG9kc73fNI7eA8VMBAAD//0SxXMMT90UdAAAAAElFTkSuQmCC"]'


class Encoder:
    def img_base64(byte_string):
        import base64

        output = str(base64.b64encode(byte_string))[2:-1]
        # output = f'<img src="data:image/png;base64,{output}">'
        output = f'["data:image/png;base64,{output}"]'
        return output

        print(output)
        return output

    def ndarray_to_png(fig):
        import numpy as np
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        from matplotlib.figure import Figure
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.gca()

        ax.text(0.0,0.0,"Test", fontsize=45)
        ax.axis('off')

        canvas.draw()       # draw the canvas, cache the renderer

        image = np.fromstring(canvas.tostring_rgb(), dtype='uint8')

        return image

    def rgb_ndarray_to_png(img):
        from PIL import Image

        import numpy as np
        # img_filename = "image.png"
        # img = Image.open(img_filename)
        # img = img.convert("RGB")
        # img.show()
        # aa  = np.array(img)
        img = Image.fromarray(img, 'RGBA')
        img.save('test.png')
        img.show()
        # alpha = Image.fromarray(img,"RGB")
        # alpha.save('my.png')
        # alpha.show()

        return img


class Getter:
    def images(endpoint, query=default_img, top_k=10):
        headers = {
            "Content-Type": "application/json",
        }

        data = '{"top_k":' + str(top_k) + ', "mode": "search", "data":' + query + "}"

        response = requests.post(
            "http://0.0.0.0:65481/api/search", headers=headers, data=data
        )
        from pprint import pprint

        pprint(response.json())

        content = response.json()["search"]["docs"][0]["topkResults"]

        img_list = []

        for doc in content:
            img = doc["matchDoc"]["uri"]
            img_list.append(img)

        return img_list


class Renderer:
    def images(content: list) -> str:
        output = ""
        try:
            for doc in content:
                html = f'<img src="{doc}">'
                output += html

            return output
        except:
            return content


class Defaults:
    endpoint = "http://0.0.0.0:65481/api/search"
    text_query = "Hello world"

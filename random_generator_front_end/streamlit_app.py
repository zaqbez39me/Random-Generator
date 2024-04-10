import streamlit as st
from config import settings
from httpx import Client
from ujson import loads
from typing import Union, List


def fetch_from_backend(client: Client, selected_source: str):
    data = {
        'source': selected_source
    }

    result = client.post("/api/random", json=data)

    if result.status_code == 200:
        result_json: dict = loads(result.text)

        if not isinstance(result_json, dict) or "number" not in result_json.keys():
            st.write("Error: Invalid JSON from the server")
        else:
            st.write(result_json['number'])
    else:
        st.write(f"Error: status code {result.status_code}")


def get_sources(client: Client) -> Union[List[str], None]:
    sources_json: dict = loads(client.get("/api/random").text)

    if not isinstance(sources_json, dict):
        return None

    if "sources" not in sources_json.keys():
        return None

    return list(sources_json['sources'])


def random_generator(client: Client):
    sources = get_sources(client)

    if sources is not None:
        x = st.selectbox("Select source to generate a random number", sources)

        st.button('Generate a random number',
                  on_click=lambda: fetch_from_backend(client, x))
    else:
        st.write("Error: Failed fetching sources from the server")


if __name__ == '__main__':
    st.title("Random Generator")
    http_client = Client(base_url=settings.BACKEND_URL, timeout=3)
    random_generator(http_client)

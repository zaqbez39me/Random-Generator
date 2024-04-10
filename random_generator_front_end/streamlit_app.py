from typing import List, Union

import streamlit as st
import ujson
from config import settings
from httpx import Client


def fetch_from_backend(client: Client, selected_source: str) -> None:
    """Fetches number from backend from specified source.
    Requires for response to be in format {"number": ...}.
    Shows it in streamlit

    Args:
        client (Client): httpx client with specified base url
        selected_source (str): source to fetch from
    Returns:
        None
    """
    result = client.get(f"/api/random/{selected_source}")
    if result.status_code == 200:
        result_json: dict = ujson.loads(result.text)
        if not isinstance(result_json, dict) or "random_number" not in result_json.keys():
            st.write("Error: Invalid JSON from the server")
        else:
            st.write(result_json["random_number"])
    else:
        st.write(f"Error: status code {result.status_code}")


def get_sources(client: Client) -> Union[List[str], None]:
    """Gets sources from backend.
    Requires for response to be in format {"sources": [...]}.


    Args:
        client (httpx.Client): Client with specified base url
    Returns:
        None: if error is found, None is returned
        list[str]: list of sources
    """
    sources_json = ujson.loads(client.get("/api/random").text)
    if not isinstance(sources_json, dict):
        return None
    if "sources" not in sources_json.keys():
        return None
    return list(sources_json["sources"])


def random_generator(client: Client) -> None:
    """Streamlit app.

    Args:
        client (httpx.Client): Client with specified base url
    Returns:
        None
    """

    sources = get_sources(client)

    if sources is not None:
        source: str = st.selectbox("Select source to generate a random number", sources)

        st.button(
            "Generate a random number",
            on_click=lambda: fetch_from_backend(client, source),
        )
    else:
        st.write("Error: Failed fetching sources from the server")


if __name__ == "__main__":
    st.title("Random Generator")
    http_client: Client = Client(base_url=settings.backend_url, timeout=3)
    random_generator(http_client)

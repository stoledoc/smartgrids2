import streamlit as st

from auth import session
from auth.password import with_password, get_token_kind
from pymongo import MongoClient

from utils import get_envvars
from fetch.collect import make_query, find_categories
from components.select_tools import selecter, select_line
from components.statics import page_desc, fig_desc
from components.download import download_csv

from visualize.figs import hour_consumption

session_state = session.get(
        password=False
        )
env_vars = get_envvars()
client = MongoClient(
        env_vars["MONGO_URL"]
        .format(
            env_vars["MONGO_USER"],
            env_vars["MONGO_PASSWORD"]
            )
        )

db = client["smartgrids2"]
collection = db["aggregated"]

@with_password(session_state)
def main():
    opts = get_token_kind(session_state)
    field_order = [
            "operador",
            "tipo_energia",
            "tipo_usuario",
            "nivel_tension_estrato",
#            "zona",
            "tipo_dia",
            "clima",
            "altitud"
            ]
    selected = {}
    for i in range(len(field_order) - 1):
        selected[field_order[i]] = selecter(
                field_order[i],
                opts
                )
        opts = find_categories(
                query=selected,
                collection=collection,
                field=field_order[i + 1]
                )
    selected[field_order[-1]] = selecter(
            field_order[-1],
            opts
            )
    data = make_query(
            query=selected,
            collection=collection
            )

    # main page
    page_desc()

    # table
    st.write(data)
    download_csv(data)

    # figure description
    fig_desc()
    # select line
    lines = select_line()

    # figure
    fig = hour_consumption(data, lines)
    st.pyplot(fig)

if __name__ == '__main__':
    main()

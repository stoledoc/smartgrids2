import os
from typing import Callable, Tuple

import streamlit as st

from auth.session import SessionState

ENV_TOKENS = ["NACIONAL_TOKEN", "CODENSA_TOKEN", "XM_TOKEN", "CEO_TOKEN", "CELSIA_TOKEN", "EPM_TOKEN"]

def is_authenticated(pwd: str) -> bool:
    return pwd in [
            os.environ[token]
            for token in ENV_TOKENS
            ]

def login(blocks: Tuple) -> str:
    style, element = blocks
    style.markdown("""
    <style>
        input { -webkit-text-security: disc; }
    </style>
    """, unsafe_allow_html=True)
    return element.text_input("Por favor ingrese el token de acceso:")


def clean_blocks(*blocks):
    for block in blocks:
        block.empty()


def with_password(session_state: SessionState):
    if session_state["password"]:
        login_blocks = None
        password = session_state["password"]
    else:
        login_blocks = st.empty(), st.empty()
        password = login(login_blocks)
        session_state["password"] = password

    def wrapper(entry_point: Callable):

        def wrapped():
            if is_authenticated(password):
                if login_blocks is not None:
                    clean_blocks(*login_blocks)
                entry_point()
            elif password:
                st.error("Token incorrecto.")
        return wrapped
    return wrapper

def get_token_kind(session_state):
    vendors = {
            "NACIONAL_TOKEN": ["nacional"],
            "CODENSA_TOKEN": ["codensa"],
            "CEO_TOKEN": ["ceo"],
            "CELSIA_TOKEN": ["celsia"],
            "EPM_TOKEN": ["epm"],
            "XM_TOKEN": ["xm"],
            }
    for token, vendor in vendors.items():
        if os.environ[token] == session_state["password"]:
            return vendor

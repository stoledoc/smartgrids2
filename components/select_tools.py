from utils import decode_opt
from typing import List
import streamlit as st

def selecter(
        message: str,
        opts: List[str]
        ):
    button = st.sidebar.selectbox(
            message,
            opts
            )
    return button

def select_line(
        ) -> List[str]:
    return st.multiselect(
            "",
            ["mean", "min", "max", "std"],
            default=["mean", "std"]
            )


from __future__ import annotations

import streamlit as st


IDLE = "idle"
LOADING = "loading"
SUCCESS = "success"
ERROR = "error"


def init_state() -> None:
    st.session_state.setdefault("view", IDLE)
    st.session_state.setdefault("current_url", "")
    st.session_state.setdefault("audit_result", None)
    st.session_state.setdefault("error_message", None)
    st.session_state.setdefault("dashboard_panel", "dashboard")
    st.session_state.setdefault("audit_history", [])


def reset_to_idle() -> None:
    st.session_state["view"] = IDLE
    st.session_state["current_url"] = ""
    st.session_state["audit_result"] = None
    st.session_state["error_message"] = None
    st.session_state["dashboard_panel"] = "dashboard"


def set_success(result: dict) -> None:
    st.session_state["view"] = SUCCESS
    st.session_state["audit_result"] = result
    st.session_state["error_message"] = None
    st.session_state["dashboard_panel"] = "dashboard"
    _remember_audit(result)


def set_error(url: str, message: str) -> None:
    st.session_state["view"] = ERROR
    st.session_state["current_url"] = url
    st.session_state["error_message"] = message
    st.session_state["audit_result"] = None


def _remember_audit(result: dict) -> None:
    history = st.session_state.setdefault("audit_history", [])
    entry = {
        "URL": result.get("url", "-"),
        "Score": result.get("score", "-"),
        "Status": result.get("status_label", "-"),
        "Datum": result.get("audit_date", "-"),
    }
    if history and history[0] == entry:
        return
    history.insert(0, entry)
    del history[10:]

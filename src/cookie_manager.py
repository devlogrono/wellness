import streamlit.components.v1 as components

_cookie_component = components.declare_component(
    "cookie_manager",
    url="http://localhost:3001",  # usando modo development
)

# _cookie_component = components.declare_component(
#     "cookie_manager",
#     path="src/components/dist"
# )

# def cookie_set(name: str, value: str, days: int = 7):
#     return _cookie_component(action="set", name=name, value=value, days=days)

# def cookie_get(name: str):
#     return _cookie_component(action="get", name=name)

# def cookie_delete(name: str):
#     return _cookie_component(action="delete", name=name)

def cookie_set(name: str, value: str, days: int = 7, **kwargs):
    return _cookie_component(
        action="set",
        name=name,
        value=value,
        days=days,
        **kwargs
    )

def cookie_get(name: str, **kwargs):
    return _cookie_component(
        action="get",
        name=name,
        **kwargs
    )

def cookie_delete(name: str, **kwargs):
    return _cookie_component(
        action="delete",
        name=name,
        **kwargs
    )
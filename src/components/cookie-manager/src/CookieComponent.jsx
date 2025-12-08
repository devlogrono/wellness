import React, { useEffect } from "react";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";

function setCookie(name, value, days) {
  const expires = new Date(Date.now() + days * 86400000).toUTCString();
  //document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=None; Secure`;
  document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=None; Secure`;

}

function getCookie(name) {
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
  return match ? match[2] : null;
}

function deleteCookie(name) {
  document.cookie = `${name}=; Max-Age=0; path=/; SameSite=None; Secure`;
}

const CookieComponent = ({ args }) => {
  
  useEffect(() => {
    if (!args) return;

    const { action, name, value, days = 7 } = args;
    let result = null;

    console.log("🔥 args recibidos:", args);

    if (action === "set") {
      setCookie(name, value, days);
    }
    else if (action === "get") {
      result = getCookie(name);
    }
    else if (action === "delete") {
      deleteCookie(name);
    }

    Streamlit.setComponentValue(result);

  }, [args]);

  useEffect(() => {
    Streamlit.setFrameHeight(0);
  }, []);

  return null;
};

export default withStreamlitConnection(CookieComponent);

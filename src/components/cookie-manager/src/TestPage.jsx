import React, { useState } from "react";

function setCookie(name, value, days) {
  const expires = new Date(Date.now() + days * 86400000).toUTCString();
  document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=None; Secure`;
}

function getCookie(name) {
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`));
  return match ? match[2] : null;
}

function deleteCookie(name) {
  document.cookie = `${name}=; Max-Age=0; path=/; SameSite=None; Secure`;
}

export default function TestPage() {
  const [value, setValue] = useState("");

  const handleSet = () => {
    setCookie("TEST_COOKIE", "HolaJose", 1);
    alert("Cookie creada!");
  };

  const handleGet = () => {
    const v = getCookie("TEST_COOKIE");
    setValue(v || "(vacía)");
  };

  const handleDelete = () => {
    deleteCookie("TEST_COOKIE");
    alert("Cookie eliminada!");
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>🔍 Test Cookie Component</h1>

      <button onClick={handleSet}>Crear Cookie</button>
      <br /><br />

      <button onClick={handleGet}>Leer Cookie</button>
      <p><b>Valor leído:</b> {value}</p>

      <br />
      <button onClick={handleDelete}>Eliminar Cookie</button>

      <hr />

      <p><b>Cookies actuales:</b> {document.cookie}</p>
    </div>
  );
}

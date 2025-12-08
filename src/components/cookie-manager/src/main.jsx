import React from "react";
import ReactDOM from "react-dom";
import CookieComponent from "./CookieComponent";

ReactDOM.render(
  <React.StrictMode>
    <CookieComponent />
  </React.StrictMode>,
  document.getElementById("root")
);

/**
import TestPage from "./TestPage";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <TestPage />
  </React.StrictMode>
);**/

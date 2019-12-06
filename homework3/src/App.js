import React from 'react';
import styles from "./app.module.scss";

const sanitize = string => {
  const map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#x27;",
    "`": "&grave;",
    "/": "&#x2F;"
  };
  const reg = /[&<>"'`/]/gi;
  return string.replace(reg, match => map[match]);
};

const App = () => {
  const [value, setValue] = React.useState("");

  return (
    <div className={styles["app"]}>
      <div className={styles["app-output"]}>
        <div className={styles["app-output__with-xss"]}>
          <div className={styles["app-output-value"]}>
            <h1>Text with XSS</h1>
            <div dangerouslySetInnerHTML={{__html: value}}/>
          </div>
        </div>
        <div className={styles["app-output__without-xss"]}>
          <div className={styles["app-output-value"]}>
            <h1>Text without XSS</h1>
            <div dangerouslySetInnerHTML={{__html: sanitize(value)}}/>
          </div>
        </div>
      </div>
      <input className={styles["app-input"]} type="text" placeholder="Enter text" value={value} onChange={(event) => {setValue(event.target.value)}} />
    </div>
  );
};

export default App;

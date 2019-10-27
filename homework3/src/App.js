import React from 'react';
import './App.css';

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
    <div className="App">
      <div className="App-output">
        <div className="App-output__withXSS">
          <div className="App-output-value">
            <h1>Text with XSS</h1>
            <div dangerouslySetInnerHTML={{__html: value}}/>
          </div>
        </div>
        <div className="App-output__withoutXSS">
          <div className="App-output-value">
            <h1>Text without XSS</h1>
            <div dangerouslySetInnerHTML={{__html: sanitize(value)}}/>
          </div>
        </div>
      </div>
      <input className="App-input" type="text" placeholder="Enter text" value={value} onChange={(event) => {setValue(event.target.value)}} />
    </div>
  );
};

export default App;

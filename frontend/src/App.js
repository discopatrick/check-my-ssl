import React, { Component } from 'react';
import './App.css';
import URLForm from './URLForm.js';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <p>
            Enter a URL to check its SSL.
          </p>
          <URLForm />
        </header>
      </div>
    );
  }
}

export default App;

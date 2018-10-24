import React, { Component } from 'react';
import { BrowserRouter, Link, Route } from 'react-router-dom';
import './App.css';
import { DomainNames } from './DomainNames.js';
import URLForm from './URLForm.js';

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div className="App">
          <header className="App-header">
            <p>
              Enter a URL to check its SSL.
            </p>
            <URLForm />
            <Link to='/domain-names'>
              View all domain names
            </Link>
            <Route exact path='/domain-names' component={DomainNames} />
          </header>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;

import React, { Component } from 'react';
import './URLForm.css';

class URLForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      actionNeeded: null,
      daysUntilSSLExpiry: null,
      value: '',
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    fetch(process.env.REACT_APP_BACKEND_BASE_URL + '/check-ssl', {
      method: 'POST',
      body: JSON.stringify({url: this.state.value}),
      headers: {'Content-Type': 'application/json'}
    })
      .then(res => res.json())
      .then(
        (result) => {
          console.log(result);
          this.setState({
            actionNeeded: result.action_needed,
            daysUntilSSLExpiry: result.days_until_ssl_expiry,
          })
        }
      )
    event.preventDefault();
  }

  render() {
    return (
      <div className="URLForm">
        <form onSubmit={this.handleSubmit}>
          <label>
            https://<input type="text" value={this.state.value} onChange={this.handleChange} />
          </label>
          <input type="submit" value="Check" />
        </form>
        <p>Days until SSL expiry: {this.state.daysUntilSSLExpiry}</p>
      </div>
    )
  }
}

export default URLForm;

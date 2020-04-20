import React from 'react';
import './SummaryPage.css';

export default class SummaryPage extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      data: null,
    }
  }

  componentDidMount() {
    this.getData()
      .then((res) => {
        const data = JSON.parse(res);
        this.setState({ data: data });
      })
      .catch(err => console.log(err));
  }

  getData = async () => {
    const response = await fetch('/database/data', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    const body = await response.text();
    return body;
  }


  render() {
    return (
      <div className="SummaryPage">
        {this.state.data}
      </div>
    );
  }
}

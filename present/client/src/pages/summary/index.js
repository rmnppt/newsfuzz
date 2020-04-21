import React from 'react';
import './SummaryPage.css';

export default class SummaryPage extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      terms: null,
      article_topics: null,
      topic_terms: null,
      topic_descriptions: null,
      sentiment_scores: null,
      article_hashes: null,
    }
  }

  componentDidMount() {
    this.getData()
      .then((res) => {
        const data = JSON.parse(res);
        this.setState({
          terms: data.terms,
          article_topics: data.article_topics,
          topic_terms: data.topic_terms,
          topic_descriptions: data.topic_descriptions,
          sentiment_scores: data.sentiment_scores,
          article_hashes: data.article_hashes,
        });
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
    console.log(response);
    const body = await response.text();
    return body;
  }


  render() {
    return (
      <div className="SummaryPage">
        {this.state.terms}
      </div>
    );
  }
}

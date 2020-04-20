const express = require('express');
const bodyParser = require('body-parser');
const { Query } = require('./database/Query');

const app = express();
const port = process.env.PORT || 5000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/api/hello', (req, res) => {
  res.send({ express: 'Hello From Express' });
});

app.post('/api/world', (req, res) => {
  console.log(req.body);
  res.send(
    `I received your POST request. This is what you sent me: ${req.body.post}`,
  );
});

app.post('/database/data', (req, res) => {
  // console.log(req.body);

  async function getData() {
    const query = new Query();
    const data = await query.data();
    return data;
  }

  getData().then((data) => {
    res.send(data);
  });
});

app.listen(port, () => console.log(`Listening on port ${port}`));

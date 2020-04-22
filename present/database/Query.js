const {Storage} = require('@google-cloud/storage');
process.env.GOOGLE_APPLICATION_CREDENTIALS = 'database/gcp_auth.json';

class Query {
  constructor() {
    this.bucketName = 'newsfuzz-analysis';
    this.srcFilename = 'daily_analysis.json';
  }

  data(req, res) {
    const storage = new Storage();
    const myBucket = storage.bucket(this.bucketName);
    const file = myBucket.file(this.srcFilename);

    // file.get(function(err, file, apiResponse) {
    //   // file.metadata` has been populated.
    // });

    //-
    // If the callback is omitted, we'll return a Promise.
    //-
    console.log('Reading File');
    var archive = file.createReadStream();

    console.log('Concat Data');
    var  buf = '';
    archive.on('data', function(d) {
      buf += d;
    }).on('end', function() {
      console.log("End");
      res.send(buf);
    });
  }

}

module.exports = {
  Query,
};

const {Storage} = require('@google-cloud/storage');
process.env.GOOGLE_APPLICATION_CREDENTIALS = 'database/gcp_auth.json';

class Query {
  constructor() {
    this.bucketName = 'newsfuzz-analysis';
    this.srcFilename = 'daily.json';
  }

  data() {
    const storage = new Storage();
    const myBucket = storage.bucket(this.bucketName);
    const file = myBucket.file(this.srcFilename);

    // file.get(function(err, file, apiResponse) {
    //   // file.metadata` has been populated.
    // });

    //-
    // If the callback is omitted, we'll return a Promise.
    //-
    return file.get().then(function(data) {
      const file = data[0];
      const apiResponse = data[1];

      console.log(file);
      console.log(apiResponse);

      return file;
    });

  }

}

module.exports = {
  Query,
};

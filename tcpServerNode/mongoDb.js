import { MongoClient, ServerApiVersion, ObjectId } from 'mongodb';
export default class DataBaseHandler {
    constructor(uri) {
      this.uri = uri;
      const mongoClient = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true, serverApi: ServerApiVersion.v1 });
      mongoClient.connect(async err => {});
    }
  }
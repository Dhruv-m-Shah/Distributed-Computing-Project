import { MongoClient, ServerApiVersion, ObjectId } from 'mongodb';
import { constants } from './constants.js';
import 'dotenv/config';
export default class DataBaseHandler {
    constructor(uri) {
      this.uri = uri;
      const mongoClient = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true, serverApi: ServerApiVersion.v1 });
      mongoClient.connect(async err => {
        this.db = mongoClient.db(process.env.DB_NAME);
      });
    }

    async clientExists(key, typeOfClient) {
        const options = {
            projection: { _id: 1 }
          };
        if(typeOfClient == constants.CLIENT_TYPES.COMPUTING_PROVIDERS) {
            let dbRes = await this.db.collection(constants.DB_COLLECTION_NAMES.COMPUTING_PROVIDERS).findOne({key: key}, options);
            console.log(dbRes);
            return dbRes != null;
        } else {
          let dbRes = await this.db.collection(constants.DB_COLLECTION_NAMES.TASK_CLIENTS).findOne({key: key}, options);
          console.log(dbRes)
          return dbRes != null;
        }
    }

    async getTaskProviderPassword(taskProviderName) {
      const options = {
        projection: { password: 1 }
      };
      let dbRes = await this.db.collection(constants.DB_COLLECTION_NAMES.COMPUTING_PROVIDERS).findOne({name: taskProviderName}, options);
      console.log(dbRes);
      return dbRes["password"];
    }
  }
import {constants} from './constants.js';

export default class Auth {
    constructor(dataBaseHandler, redisHandler, localCacheHandler) {
        this.dataBaseHandler = dataBaseHandler;
        this.redisHandler = redisHandler;
        this.localCacheHandler = localCacheHandler;
    }

    async checkValidUser(typeOfRequest, key) {
        if([constants.TCP_REQUEST_TYPES.HEART_BEAT, constants.TCP_REQUEST_TYPES.TASK_FINISHED].includes(typeOfRequest)) {
            return await this.verifyComputingProvider(key, constants.CLIENT_TYPES.COMPUTING_PROVIDERS);
        } else if (typeOfRequest in [constants.TASK]) {
            return await this.verifyTaskClient(key);
        }
    }

    async verifyComputingProvider(key, typeOfClient) {
        if(this.localCacheHandler.clientExists(key, typeOfClient)) {
            console.log("in local cache");
            return true;
        } else if(await this.redisHandler.clientExists(key, typeOfClient)) {
            console.log("in redis");
            this.localCacheHandler.storeKey(key, typeOfClient);
            return true;
        } else if(await this.dataBaseHandler.clientExists(key, typeOfClient)) {
            console.log("in db");
            this.redisHandler.storeKey(key, typeOfClient);
            this.localCacheHandler.storeKey(key, typeOfClient);
            return true;
        } else {
            return false;
        }
    }
  }
import { createClient } from 'redis';
import CacheHandler from "./cacheHandler.js"
import { constants } from "./constants.js"

export default class RedisHandler extends CacheHandler {
    constructor(url) {
        super();
        this.url = url;
        this.client = createClient({
            url: url
        });
        this.client.connect();
    }

    async clientExists(key, typeOfClient) {
        let keyValue = await this.client.get(key);
        if(keyValue == typeOfClient){
            return true;
        } else {
            return false;
        }
    }

    async storeKey(key, value, keyExpiry = constants.CACHE_CONSTANTS.TIME_TO_EXPIRE_KEY_IN_SEC) {
        await this.client.set(key, value, 'EX', keyExpiry);
    }

    async storeInSortedSet(setName, key, value) {
        console.log(setName, key, value);
        await this.client.zAdd(setName, [{score: key, value: value}]);
    }

    async removeFromSortedSet(setName, key) {
        await this.client.zRem(setName, key);
    }
  }
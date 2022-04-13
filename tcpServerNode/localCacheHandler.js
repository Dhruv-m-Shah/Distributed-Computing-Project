import NodeCache from 'node-cache';
import CacheHandler from "./cacheHandler.js"
import {constants} from './constants.js';

export default class LocalCacheHandler extends CacheHandler {
    constructor() {
        super();
        this.myCache = new NodeCache();
    }

    clientExists(key, typeOfClient) {
        let keyValue = this.myCache.get(key);
        if(keyValue == typeOfClient){
            return true;
        } else {
            return false;
        }
    }

    storeKey(key, value, keyExpiry = constants.CACHE_CONSTANTS.TIME_TO_EXPIRE_KEY_IN_SEC) {
        this.myCache.set(key, value, keyExpiry);    
    }
  }
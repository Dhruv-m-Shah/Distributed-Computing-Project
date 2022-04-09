import NodeCache from 'node-cache';
import CacheHandler from "./cacheHandler.js"
export default class LocalCacheHandler extends CacheHandler {
    constructor() {
        super();
        this.myCache = new NodeCache();
    }
  }
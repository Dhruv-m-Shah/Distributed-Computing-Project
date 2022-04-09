import { createClient } from 'redis';
import CacheHandler from "./cacheHandler.js"

export default class RedisHandler extends CacheHandler {
    constructor(url) {
        super();
        this.url = url;
        const client = createClient({
            url: url
        });
        client.connect();
    }
  }
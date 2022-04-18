import { constants } from "./constants.js"

export default class TcpParser {
    constructor(url) {
        this.buffer = Buffer.alloc(0);
    }

    appendData(buf) {
        this.buffer = Buffer.concat([this.buffer, buf]);
    }

    checkIfMessageReceived() {
        try {
        let contentLengthBytes = null;
        console.log(this.buffer.length);
        console.log(this.buffer);
        if(this.buffer.length >= 4){
            contentLengthBytes = Number(this.buffer.toString('utf-8',0, 4)); // get first 4 bytes which specify content length.
        } else {
            return null;
        }
        console.log(contentLengthBytes);
        if(contentLengthBytes != null && this.buffer.length >= 4 + contentLengthBytes){
            let message = Buffer.toString(4, 4+contentLengthBytes);
            this.buffer = this.buffer.subarray(4+contentLengthBytes);
            return message;
        } else {
            return null;
        }
    } catch(e) {
        console.log(e);
    }
    }

  }
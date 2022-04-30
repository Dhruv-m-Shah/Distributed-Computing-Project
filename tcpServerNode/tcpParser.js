import { constants } from "./constants.js"

export default class TcpParser {
    constructor() {
        this.buffer = Buffer.alloc(0);
    }

    appendData(buf) {
        this.buffer = Buffer.concat([this.buffer, buf]);
    }

    checkIfMessageReceived() {
        try {
            let contentLengthBytes = null;
            if(this.buffer.length >= constants.CONTENT_SIZE_LEN) {
                contentLengthBytes = Number(this.buffer.toString(constants.TCP_ENCODING, 0,
                                                                 constants.CONTENT_SIZE_LEN));
            } else {
                return null;
            }
            if(contentLengthBytes != null && this.buffer.length >= constants.CONTENT_SIZE_LEN + contentLengthBytes) {
                let message = this.buffer.toString(constants.TCP_ENCODING, constants.CONTENT_SIZE_LEN,
                                                constants.CONTENT_SIZE_LEN+contentLengthBytes);
                this.buffer = this.buffer.subarray(constants.CONTENT_SIZE_LEN+contentLengthBytes);
                return message;
            } else {
                return null;
            }
        } catch(e) {
            console.log(e);
        }
    }

    formatTcpMessage(msg) {
        let msgLenInBytes = Buffer.byteLength(msg, 'utf8').toString();
        if(msgLenInBytes.length > 16) {
            return constants.RESPONSES.MESSAGE_SIZE_EXCEEDED;
        }
        while(msgLenInBytes.length < 16) {
            msgLenInBytes = "0" + msgLenInBytes;
        }
        return msgLenInBytes + JSON.stringify(msg);
    }
}
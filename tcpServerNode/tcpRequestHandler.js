
import {constants} from './constants.js';
import TcpParser  from './tcpParser.js';

function checkStringArray(arr) {
    for(let i = 0; i < arr.length; i++) {
        if(typeof(arr[i]) != "string") {
            return false;
        }
        return true;
    }
}

export default class TcpRequestHandler {
    constructor(dataBaseHandler, redisHandler, localCacheHandler, auth) {
        this.dataBaseHandler = dataBaseHandler;
        this.redisHandler = redisHandler;
        this.localCacheHandler = localCacheHandler;
        this.auth = auth;
        this.nameToSocket = {};
        this.tcpParser = new TcpParser(); 
    }

    handleTcpRequest(rawReq, socket) {
        try {
            const jsonParsedString = JSON.parse(rawReq.toString());
            const typeOfReq = this.parseRequest(jsonParsedString);
            if(typeOfReq == constants.RESPONSES.ERROR_REQUEST_PARSE) {
                console.log("Parse error")
                socket.write("ERROR"); // Come up with better error message;
                socket.end();
                return constants.RESPONSES.UNKNOWN_ERROR;
            }
        
            if(!this.auth.checkValidUser(typeOfReq, jsonParsedString.key)) {
                socket.write("Invalid key");
                console.log("Invalid key")
                socket.end();
            }
            this.handleRequest(jsonParsedString, typeOfReq, socket);
            
        } catch (e) {
            console.log(e);
            return constants.RESPONSES.UNKNOWN_ERROR;
        }
    }

    parseRequest(req) {
        if("type" in req) {
            const typeOfRequest = req["type"];
            
            if(typeOfRequest == constants.TCP_REQUEST_TYPES.HEART_BEAT){
                return this.verifyHeartBeat(req);
            } else if(typeOfRequest == constants.TCP_REQUEST_TYPES.TASK) {
                return this.verifyTask(req);
            } else if (typeOfRequest == constants.TCP_REQUEST_TYPES.TASK_FINISHED) {
                console.log("ASDASDASDASD")
                return this.verifyTaskFinished(req); 
            } else {
                return constants.RESPONSES.ERROR_REQUEST_PARSE;
            }
        } else {
            return constants.RESPONSES.ERROR_REQUEST_PARSE;
        }
    }
 
    verifyHeartBeat(jsonParsedString) {
        let isValid = true;
        isValid = isValid && (Object.keys(jsonParsedString).length == constants.TCP_REQUEST_TYPES.NUM_KEYS_IN_HEARTBEAT);
        isValid = isValid && ("type" in jsonParsedString
                                && "key" in jsonParsedString
                                && "tasksInQueue" in jsonParsedString
                                && "providerState" in jsonParsedString);
        if(!isValid) {
            return constants.RESPONSES.ERROR_REQUEST_PARSE
        }
        isValid = isValid && typeof(jsonParsedString["type"]) == "string" && typeof(jsonParsedString["key"]) == "string"
                          && typeof(jsonParsedString["tasksInQueue"]) == "number" && typeof(jsonParsedString["providerState"]) == "string"
                          && typeof(jsonParsedString["name"] == "string");
        
        if(isValid) {
            return constants.TCP_REQUEST_TYPES.HEART_BEAT;
        } else {
            return constants.RESPONSES.ERROR_REQUEST_PARSE;
        }
    }

    verifyTask(req) {
        let isValid = true;
        isValid = isValid && (Object.keys(req).length == constants.TCP_REQUEST_TYPES.NUM_KEYS_IN_TASK)
        isValid = isValid && ("type" in req && "key" in req && "taskName" in req && "computingProviderNames" in req
                          && "computingProviderPasswords" in req && "pyScripts" in req && "taskClientName" in req);
        if(!isValid) {
            return constants.RESPONSES.ERROR_REQUEST_PARSE;
        }
        isValid = isValid && typeof(req["type"]) == "string" && typeof(req["key"]) == "string"
                          && typeof(req["taskName"]) == "string" && typeof(req["taskClientName"]) == "string" 
                          && Array.isArray(req["computingProviderNames"])
                          && Array.isArray(req["computingProviderPasswords"]) && Array.isArray(req["pyScripts"])
                          && checkStringArray(req["computingProviderNames"]) && checkStringArray(req["computingProviderPasswords"])
                          && checkStringArray(req["pyScripts"]);
        if(isValid) {
            return constants.TCP_REQUEST_TYPES.TASK;
        } else {
            return constants.RESPONSES.ERROR_REQUEST_PARSE;
        }
    }

    verifyTaskFinished(req) {
        console.log(req)
        let isValid = true;
        isValid = isValid && (Object.keys(req).length == constants.TCP_REQUEST_TYPES.TCP_REQUEST_TYPES_NUM_KEYS_IN_TASK_FINISHED);
        isValid = isValid && ("key" in req && "name" in req && "taskName" in req && "taskIssuerName" in req 
                                           && "taskStatus" in req && "type" in req);
        if(!isValid) {
            console.log("ASD")
            return constants.RESPONSES.ERROR_REQUEST_PARSE;
        }
        isValid = isValid && typeof(req["key"] == "string" && typeof(req["name"]) == "string" && typeof(req["taskName"]) == "string"
                                    && req["taskIssuerName"] == "string" && typeof("taskStatus") == "string" && typeof("type") == "string");
        if(isValid) {
            return constants.TCP_REQUEST_TYPES.TASK_FINISHED;
        } else {
            return constants.RESPONSES.ERROR_REQUEST_PARSE;
        }
    }

    handleRequest(req, typeOfRequest, socket) {
        if(typeOfRequest == constants.TCP_REQUEST_TYPES.HEART_BEAT) {
            this.handleHeartBeatRequest(req, socket);
        } else if(typeOfRequest == constants.TCP_REQUEST_TYPES.TASK) {
            this.handleTaskRequest(req, socket);
        } else if (typeOfRequest == constants.TCP_REQUEST_TYPES.TASK_FINISHED) {
            this.handleTaskFinishedRequest(req, socket); 
        }
    }

    handleTaskFinishedRequest(req, socket) {
        if(!(req["taskIssuerName"] in this.nameToSocket)) {
            constants.RESPONSES.TASK_CLIENT_NOT_FOUND
        }
        delete req.key;
        this.nameToSocket[req["taskIssuerName"]].write(this.tcpParser.formatTcpMessage(req));
    }

    handleHeartBeatRequest(req, socket) {
        // update computing provider state
        this.redisHandler.storeKey(req.key, req.providerState);
        if(req.providerState != constants.COMPUTING_PROVIDER_STATES.OK) {
            this.redisHandler.removeFromSortedSet(constants.CACHE_CONSTANTS.SORTED_SET_NAME, req.key);
        } else {
            this.redisHandler.storeInSortedSet(constants.CACHE_CONSTANTS.SORTED_SET_NAME, req.tasksInQueue, req.key);
        }
        this.nameToSocket[req["name"]] = socket;
    }

    async handleTaskRequest(req, socket) {
        // check that all tasks provider's socket connections exist.
        this.nameToSocket[req["taskClientName"]] = socket;
        for(let i = 0; i < req["computingProviderNames"].length; i++) {
           if(!(req["computingProviderNames"][i] in this.nameToSocket)) {
               return constants.RESPONSES.PROVIDER_NOT_FOUND;
           }
           let taskProviderPassword = await this.dataBaseHandler.getTaskProviderPassword(req["computingProviderNames"][i]);
           if(req["computingProviderPasswords"][i] != taskProviderPassword) {
               return constants.RESPONSES.PROVIDER_PASSWORD_INCORRECT;
           }
        }
        for(let i = 0; i < req["computingProviderNames"].length; i++) {
            let computingProviderName = req["computingProviderNames"][i];
            let socket = this.nameToSocket[computingProviderName]
            let taskRequest = {
                type: "task",
                taskName: req["taskName"],
                taskIssuerName: req["taskClientName"],
                pythonScript: req["pyScripts"][i]
            }
            console.log(this.tcpParser.formatTcpMessage(JSON.stringify(taskRequest)))
            socket.write(this.tcpParser.formatTcpMessage(taskRequest));
        }
    }
    
  }
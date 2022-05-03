export const constants = {
    TCP_REQUEST_TYPES: {
        HEART_BEAT : "heartbeat",
        TASK : "task",
        TASK_FINISED : "taskFinished",
        NUM_KEYS_IN_HEARTBEAT : 5,
        NUM_KEYS_IN_TASK : 7,
        TCP_REQUEST_TYPES_NUM_KEYS_IN_TASK_FINISED: 6
    },
  CACHE_CONSTANTS: {
    TIME_TO_EXPIRE_KEY_IN_SEC : 3600,
    SORTED_SET_NAME: "tasksInQueue"  
  },
  CLIENT_TYPES: {
      COMPUTING_PROVIDERS: "computing-providers",
      TASK_CLIENTS: "task-clients"
  },
  COMPUTING_PROVIDER_STATES: {
      OK: "OK",
      ERROR_STATE: "ERROR_STATE"
  },
  DB_COLLECTION_NAMES: {
    COMPUTING_PROVIDERS: "computing-providers",
    TASK_CLIENTS: "task-clients"
  },
  RESPONSES: {
      UNKNOWN_ERROR: "UNKNOWN_ERROR",
      SUCCESS: "SUCCESS",
      ERROR_REQUEST_PARSE : "errorRequestParse",
      PROVIDER_NOT_FOUND: "Provider name was not found",
      PROVIDER_PASSWORD_INCORRECT: "Provider password was incorrect",
      MESSAGE_SIZE_EXCEEDED: "Program is too long",
      TASK_CLIENT_NOT_FOUND: "Task provider was not found"
  },
  MAX_MESSAGE_SIZE : 100000000, // 100 mb
  CONTENT_SIZE_LEN : 16,
  TCP_ENCODING: 'utf-8'
};
import 'dotenv/config';
import tls from 'tls'
import fs from 'fs';
import DataBaseHandler from './dataBaseHandler.js';
import RedisHandler from './redisHandler.js';
import TcpRequestHandler from './tcpRequestHandler.js';
import LocalCacheHandler from './localCacheHandler.js';
import Auth from './auth.js'
import TcpParser  from './tcpParser.js';
import {constants} from './constants.js';

var dataBaseHandler = new DataBaseHandler(`mongodb+srv://${process.env.DB_USER}:${process.env.DB_PASS}@cluster0.ob8gc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority`);
var redisHandler = new RedisHandler(process.env.REDIS_URL);
var localCacheHandler = new LocalCacheHandler();
var auth = new Auth(dataBaseHandler, redisHandler, localCacheHandler);
var tcpRequestHandler = new TcpRequestHandler(dataBaseHandler, redisHandler, localCacheHandler, auth);
var tcpParser = new TcpParser();
const port = 8000;

const options = {
    key: fs.readFileSync('../certs/server/server.key'),
    cert: fs.readFileSync('../certs/server/server.crt'),
    ca: fs.readFileSync('../certs/ca/ca.crt'), // authority chain for the clients
    requestCert: false, // ask for a client cert
    //rejectUnauthorized: false, // act on unauthorized clients at the app level
};

var server = tls.createServer(options, (socket) => {
  socket.on('data', (data) => {
    try {
      tcpParser.appendData(data);
      let msg = tcpParser.checkIfMessageReceived();
      if(msg!=null) {
        tcpRequestHandler.handleTcpRequest(msg, socket);
      }
    } catch(e) {
      console.log(e);
    }
  });
})

.on('connection', function(c)
{
    console.log('insecure connection');
})

.on('secureConnection', function (c)
{
    // c.authorized will be true if the client cert presented validates with our CA
    console.log('secure connection; client authorized: ', c.authorized);
})

.listen(port, function() {
    console.log('server listening on port ' + port + '\n');
});
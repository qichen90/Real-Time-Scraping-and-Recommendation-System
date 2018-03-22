const { createLogger, format, transports } = require('winston');

var logger = createLogger({
  format: format.combine(
    format.timestamp(),
    format.json()
  ),
  transports: [
    new transports.Console(),
    new transports.File({ filename: './log/error.log'}),
    new transports.File({ filename: './log/info.log'})
  ]
});

module.exports = logger;

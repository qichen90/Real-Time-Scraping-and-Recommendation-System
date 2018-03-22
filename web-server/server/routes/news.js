var express = require('express');
var router = express.Router();
var logger = require('../logger');
var rpc_client = require('../rpc_client/rpc_client')


router.get('/userId/:userId/pageNum/:pageNum', (req, res, next) => {
  logger.log({
    level: 'info',
    message: 'load more news'
  });
  userId = req.params['userId'];
  pageNum = req.params['pageNum'];
  
  rpc_client.getNewsSummariesForUser(userId, pageNum, function(response) {
    res.json(response);
  });
});

// send click to ClickLogProcessor
router.post('/userId/:userId/newsId/:newsId', (req, res, next) => {
  userId = req.params['userId'];
  newsId = req.params['newsId'];

  rpc_client.logNewsClickForUser(userId, newsId);
  res.status(200);
});

module.exports = router;
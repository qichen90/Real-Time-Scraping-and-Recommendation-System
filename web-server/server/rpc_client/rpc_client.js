var jayson = require('jayson');

var client = jayson.client.http({
    port: 4040,
    hostname: 'localhost'
});

function add(num1, num2, callback) {
    client.request('add', [num1, num2], function(err, error, response) {
        if(err) throw err;
        callback(response);
    });
}

function getNewsSummariesForUser(userId, pageNum, callback) {
    client.request('getNewsSummariesForUser', [userId, pageNum], function(err, error, response){
        if(err) throw err;
        console.log(response);
        callback(response);
    });
}

function logNewsClickForUser(userId, newsId){
    client.request('logNewsClickForUser', [userId, newsId], function(err, error, response) {
        if(err) throw err;
        console.log(response);
    });
}

module.exports = {
    add: add,
    getNewsSummariesForUser: getNewsSummariesForUser,
    logNewsClickForUser: logNewsClickForUser
};
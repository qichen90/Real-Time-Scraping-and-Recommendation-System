var test = require('./rpc_client')

test.add(1, 2, function(response){
    console.log(response);
    console.assert(response == 3);
});

test.getNewsSummariesForUser('test', 1, function(response){
    console.assert(response != null);
});

test.logNewsClickForUser('test', '6rawLZRh3cZMJ51/Vi/7dA==\n');
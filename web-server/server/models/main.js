const mongoose = require('mongoose');

module.exports.connect = (uri) => {
    mongoose.connect(uri);
    mongoose.connection.on('error', (err) => {
        console.error('Mongoose connection err: '+ err);
        process.exit(1);
    });
    require('./user');
};
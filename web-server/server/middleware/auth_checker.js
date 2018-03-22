const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const config = require('../config/config.json');

module.exports = (req, res, next) => {
    console.log('auth_checker req: ' + req.headers);
    if(!req.headers.authentication) {
        return res.status(401).end();
    }
    const token = req.headers.authentication.split(' ')[1];
    console.log('token: ' + token);

    return jwt.verify(token, config.jwtSecret, (err, decoded) => {
        if(err) { 
            return res.status(401).end();
        }
        const id = decoded.sub;

        return User.findById(id, (errUser, user) => {
            if(errUser || !user) {
                return res.status(401).end();
            }
            return next();
        });
    });
};
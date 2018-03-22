const PassportLocalStrategy = require('passport-local').Strategy;
const User = require('mongoose').model('User');
const jwt = require('jsonwebtoken');
const config = require('../config/config.json');

module.exports = new PassportLocalStrategy({
    usernameField: 'email',
    passwordField: 'password',
    session: false,
    passReqToCallback: true
}, (req, email, password, done) => {
    const userData = {
        email: email.trim(),
        password: password
    };

    return User.findOne({email: userData.email}, (err, user) => {
        if(err){
            return done(err);
        }
        if(!user){
            const error = new Error('Incorrect email or password');
            error.name = 'IncorrectCredentialErros';
            return done(error);
        }
        return user.comparePassword(userData.password,(passwordErr, isMatched) => {
            if(passwordErr){
                return done(passwordErr);
            }
            if(!isMatched) {
                const error = 'Incorrect email or password';
                error.name = 'IncorrectCredentialErrors';
                return done(error);
            }
            console.log(isMatched);
            const payload = {
                sub: user._id
            };
            const token = jwt.sign(payload, config.jwtSecret);
            
            return done(null, token, null);
        });
    });
});

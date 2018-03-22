const PassportLocalStrategy = require('passport-local').Strategy;
const User = require('mongoose').model('User');

module.exports = new PassportLocalStrategy({
    usernameField: 'email',
    passwordField: 'password',
    passReqToCallback: true
}, (req, email, password, done) => {
    const userData = {
        email: email.trim(),
        password: password
    };
    const newUser = new User(userData);
    // mongoDB check duplicates internally
    newUser.save((err) => {
        console.log('Save new user!');
        if(err) {
            return done(err);
        }
        return done(null);
    });
});
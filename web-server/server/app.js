var express = require('express');
var path = require('path');
var bodyParse = require('body-parser');
var cors = require('cors');

var auth = require('./routes/auth');
var index = require('./routes/index');
var news = require('./routes/news');
var app = express();
var logger = require('./logger');
var passport = require('passport');

app.use(bodyParse.json());
// connect with MongoDb
var config = require('./config/config.json');
require('./models/main.js').connect(config.mongoDbUri);

var authchecker = require('./middleware/auth_checker');

// register passport
app.use(passport.initialize());
var localLoginStrategy = require('./passport/login_passport');
var localSignupStrategy = require('./passport/signup_passport');
passport.use('local-login', localLoginStrategy);
passport.use('local-signup', localSignupStrategy);

// cross origin problem
app.use(cors());
// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use('/static', express.static(path.join(__dirname, '../client/build/static')));

app.use('/', index);
app.use('/auth', auth);
app.use('/news', authchecker); 
app.use('/news', news);

// catch 404
app.use(function(req, res, next) {
  res.status(404);
});

module.exports = app;

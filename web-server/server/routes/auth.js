var express = require('express');
var router = express.Router();
var passport = require('passport');
var validator = require('validator');

router.post('/login', (req, res, next) => {
    const validateResult = validateLoginForm(req.body);
    if(!validateResult.success){
        return res.status(400).json({
            success: false,
            message: validateResult.message,
            errors: validateResult.errors
        });
    }
    return passport.authenticate('local-login', (err, token, userData) => {
        if(err) {
            if(err.name == 'IncorrectCredentialErrors'){
                return res.status(400).json({
                    success: false,
                    message: err.message
                });
            }
            return res.status(400).json({
                success: false,
                message: 'Could not process the form ' + err.message
            });
        }
        return res.json({
            success: true,
            message: 'You have successfully logged in.',
            token,
            user: userData
        });
    })(req, res, next);
});

router.post('/signup', (req, res, next) => {
    const validateForm = validateSignupForm(req.body);
    if(!validateForm.success) {
        return res.status(400).json({
            success: false,
            errors: validateForm.errors,
            message: validateForm.message
        });
    }
    return passport.authenticate('local-signup', (err) => {
        if(err) {
            console.log(err);
            if(err.name == 'MongoError' && err.code === 11000){
                return res.status(409).json({
                    success: false,
                    message: 'Check the errors',
                    errors: {
                        email: 'This email is already existing'
                    }
                });
            }
            return res.status(400).json({
                success: false,
                message: 'Cound not process the form'
            });
        }
        return res.json({
            success: true,
            message: 'You have successfully sign up. Please log in now.'
        });
    })(req, res, next);
});

/*
  validate the login form: check email and password, return errors, validation, message
*/
function validateLoginForm(payload) {
    const errors = {};
    let isFormValid = true;
    let message = '';

    if(!payload || typeof payload.email !== 'string' || payload.email.trim().length === 0){
        isFormValid = false;
        console.log("error email");
        
        errors.email = 'Please provide your email address.';
    }

    if(!payload || typeof payload.password !== 'string' || payload.password.length === 0){
        isFormValid = false;
        console.log("error pwd");
        errors.password = 'Please provide your password.';
    }

    if(!isFormValid){
        message = 'Check the form for errors.';
    }
    return {
        success: isFormValid,
        errors,
        message
    };
}
/*
  validate the signup form: check email and password, return errors, validation, message
*/
function validateSignupForm(payload) { 
    const errors = {};
    let isFormValid = true;
    let message = '';

    if(!payload || typeof payload.email !== 'string' || !validator.isEmail(payload.email)){
        isFormValid = false;
        errors.email = 'Please provide valid email.';
    }
    if(!payload || typeof payload.password !== 'string' || payload.password.length < 8){
        isFormValid = false;
        errors.password = 'Please provide valid password.';
    }
    if(!isFormValid){
        message = 'Please check the sign up form for errors';
    }
    return {
        success: isFormValid,
        errors,
        message
    }
}

module.exports = router;
import LoginForm from './LoginForm';
import React from 'react';
import Auth from '../Auth/Auth';
import PropTypes from 'prop-types';

class LoginPage extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            errors: {},
            user: {
                email: '',
                password: ''
            }
        };
    }

    processForm(e) {
        e.preventDefault();
        const email = this.state.user.email;
        const password = this.state.user.password;
        
        // Post to web server
        const url = 'http://' + window.location.hostname + ':3000/auth/login';
        const request = new Request (
            url,
            {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );

        fetch(request).then(res => {
            if(res.status === 200) {
                this.setState({errors: {}});
                res.json().then(json => {
                    Auth.authenticateUser(json.token, email);
                    this.context.router.replace('/');
                });
            } else {
                res.json().then(json => {
                    const errors = json.errors? json.errors: {};
                    errors.summary = json.message;
                    this.setState({errors: errors});
                });
            }
        })
    }

    changeUser(e) {
        const field = e.target.name; // get changed field
        const user = this.state.user;
        user[field] = e.target.value;
        this.setState({user: user});
    }

    render() {
        return (<LoginForm 
        onSubmit={(e) => this.processForm(e)}
        onChange={(e) => this.changeUser(e)}
        errors={this.state.errors}
        user={this.state.user}/>);
    }
};

LoginPage.contextTypes = {
    router: PropTypes.object.isRequired
};

export default LoginPage;
import PropTypes from 'prop-types';
import React from 'react';
import SignupForm from './SignupForm';

class SignupPage extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            errors: {},
            user: {
                email: '',
                password: '',
                confirmed_password: ''
            }
        };
    }

    processForm(e) {
        e.preventDefault();

        const email = this.state.user.email;
        const password = this.state.user.password;
        const confirmed_password = this.state.user.confirmed_password;
        console.log('email: ' + email + '; password: ' + password);
        console.log('confirmed_password: ' + confirmed_password);   
        if(password !== confirmed_password){
            return ;
        }    
        
        const url = "http://" + window.location.hostname + ":3000/auth/signup";
        const request = new Request(
            url,
            {
                method: 'POST',
                headers: {
                    'Accept': 'Application/json',
                    'Content-Type': 'Application/json'
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
                this.context.router.replace('/login');
            } else {
                res.json().then(json => {
                    const errors = json.erros? json.errors: {};
                    errors.summary = json.message;
                    this.setState({errors});
                });
            }
        });
    }

    changeUser(e) {
        const field = e.target.name;
        const user = this.state.user;
        user[field] = e.target.value;
        this.setState({user: user});

        if(field === 'confirmed_password'){
            if(this.state.user.password !== this.state.user.confirmed_password){
                const errors = this.state.errors;
                errors.confirmed_password = "Password doesn't match";
                this.setState({errors:errors});
            }else{
                const errors = this.state.errors;
                errors.confirmed_password = '';
                this.setState({errors: errors});
            }
        }
    }

    render() {
        return (<SignupForm
            onSubmit={(e) => {this.processForm(e)}}
            onChange={(e) => {this.changeUser(e)}}
            errors={this.state.errors}
            user={this.state.user}
        />);
    }
};
SignupPage.contextTypes = {
    router: PropTypes.object.isRequired
};

export default SignupPage;
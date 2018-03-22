import './LoginForm.css'
import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router';

const LoginForm = ({
    onSubmit,
    onChange,
    errors,
    user}) => (
        <div className='container'>
            <div className='card-panel login-form'>
                <form className='col s12' action='/' onSubmit={onSubmit}>
                    <h4 className='center-align'>Login</h4>
                    {errors.summary && <div className='row'><p className='error-message'>{errors.summary}</p></div>}
                    <div className='row'>
                        <div className='input-field col s12'>
                            <input id='email' type='email' name='email' className='validate' onChange={onChange}/>
                            <label htmlFor='email'>Email</label>
                        </div>
                    </div>
                    {errors.email && <div className='row'><p className='error-message'>{errors.email}</p></div>}
                    <div className='row'>
                        <div className='input-field col s12'>
                            <input id='password' type='password' name='password' className='validate' onChange={onChange}/>
                            <label htmlFor='password'>Password</label>
                        </div>
                    </div>
                    {errors.password && <div className='row'><p className='error-message'>{errors.password}</p></div>}
                    <div className='row right-align'>
                        <input className='btn waves-effect waves-light teal lighten-3' type='submit' value='Log in'/>
                    </div>
                    <div className='row right-align'>
                        <p className='right-align'>New to NewsNow? <Link to='/signup'>Sign Up</Link></p>
                    </div>
                </form>
            </div>
        </div>
    );
LoginForm.propTypes = {
    onSubmit: PropTypes.func.isRequired,
    onChange: PropTypes.func.isRequired,
    errors: PropTypes.object.isRequired,
    user: PropTypes.object.isRequired
};
export default LoginForm;
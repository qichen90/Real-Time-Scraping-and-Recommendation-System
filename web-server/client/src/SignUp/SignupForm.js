import './SignupForm.css'
import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router';

const SignupForm = ({
    onSubmit,
    onChange,
    errors,
    user
    }) => (
        <div className='container'>
            <div className='card-panel signup-form'>
                <form className='col s12' action='/' onSubmit={onSubmit}>
                    <h4 className='center-align'>Sign Up</h4>
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
                    <div className='row'>
                        <div className='input-field col s12'>
                            <input id='confirmed_password' type='password' name='confirmed_password' className='validate' onChange={onChange}/>
                            <label htmlFor='confirmed_password'>Comfirm Password</label>
                        </div>
                    </div>
                    {errors.confirmed_password && <div className='row'><p className='error-message'>{errors.confirmed_password}</p></div>}
                    <div className='row right-align'>
                        <input className='btn waves-effect waves-light teal lighten-3' type='submit' value='Sign up'/>
                    </div>
                    <div className="row">
                        <p className="right-align"> Already have an account? <Link to="/login">Login</Link></p>
                    </div>
                </form>
            </div>
        </div>
    );
SignupForm.propTypes = {
    onSubmit: PropTypes.func.isRequired,
    onChange: PropTypes.func.isRequired,
    errors: PropTypes.object.isRequired,
    user: PropTypes.object.isRequired
};
export default SignupForm;
import 'materialize-css/dist/css/materialize.min.css'
import 'materialize-css/dist/js/materialize.js';
import './Base.css';
import React from 'react';
import { Link }from 'react-router';
import Auth from '../Auth/Auth';

class Base extends React.Component {
    render(){
        return (
            <div>
                <nav className="nav-wrapper  teal lighten-3">
                    <a href="/" className="brand-logo">News Now</a>
                    <ul id ="nav-mobile" className="right">
                        {Auth.isAuthenticated()? 
                            (<div>
                                <li><Link to="/aboutme">AboutMe</Link></li>
                                <li>{Auth.getEmail()}</li>
                                <li><Link to="/logout">Log Out</Link></li>
                            </div>)
                            :
                            (<div>
                                <li><Link to="/aboutme">About Me</Link></li>
                                <li><Link to="/login">Login</Link></li>
                                <li><Link to="/signup">Signup</Link></li>
                            </div>)
                        }
                    </ul>
                </nav>
                <br />
                {this.props.children}
            </div>
        );
    };
};

export default Base;
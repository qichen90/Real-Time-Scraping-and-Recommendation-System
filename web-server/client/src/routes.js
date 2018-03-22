import App from './App/App';
import Auth from './Auth/Auth';
import Base from './Base/Base';
import Login from './Login/LoginPage';
import Signup from './SignUp/SignupPage';
import AboutMe from './AboutMe/AboutMe';

const routes = {
    component: Base,
    childRoutes: [
        {
            path: '/',
            getComponent: (location, callback) => {
                if(Auth.isAuthenticated()) {
                    callback(null, App);
                }else {
                    callback(null, Login);
                }
            }
        },
        {
            path: '/login',
            component: Login
        },
        {
            path: '/signup',
            component: Signup
        },
        {
            path: '/logout',
            onEnter: (nextState, replace) => {
                Auth.deauthenticateUser();
                replace('/');
            }
        },
        {
            path: '/aboutme',
            component: AboutMe
        }
    ]
};

export default routes;
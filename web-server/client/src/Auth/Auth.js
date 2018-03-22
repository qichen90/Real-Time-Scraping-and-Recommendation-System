class Auth {
    // authenticate User using token and email from node server
    static authenticateUser(token, email) {
        localStorage.setItem('token', token);
        localStorage.setItem('email', email);
    }
    // deauthenticate User after log out
    static deauthenticateUser(){
        localStorage.removeItem('token');
        localStorage.removeItem('email');
    }
    // check if the user is authendicated
    static isAuthenticated() {
        return this.getToken() !== null;
    }
    // get Authenticated User's email
    static getEmail() {
        return localStorage.getItem('email');
    }
    // get token
    static getToken() {
        return localStorage.getItem('token')
    }
}
export default Auth;
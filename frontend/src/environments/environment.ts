/* @TODO replace with your variables (DONE)
 * ensure all variables on this page match your project
 */

export const environment = {
    production: false,
    apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
    auth0: {
        url: 'kcruz.us', // the auth0 domain prefix
        audience: 'coffee-shop', // the audience set for the auth0 app
        clientId: 'S5atBMSIKiy7Jt0ma4A5NHB8QSPVkgLH', // the client id generated for the auth0 app
        callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
    }
};

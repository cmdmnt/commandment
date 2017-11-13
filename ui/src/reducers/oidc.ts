// redux-oidc configuration
import createOidcMiddleware, { createUserManager } from "redux-oidc";

const config = {
    authority: "https://accounts.google.com",
    automaticSilentRenew: true,
    client_id: window.OIDC_CLIENT_ID,
    filterProtocolClaims: true,
    loadUserInfo: true,
    post_logout_redirect_uri: `${window.location.protocol}//${window.location.hostname}:${window.location.port}/login`,
    redirect_uri: window.OIDC_REDIRECT_URI || `${window.location.protocol}//${window.location.hostname}:${window.location.port}/sso/oidc/callback`,
    response_type: "id_token token",
    scope: "openid profile",
    silent_redirect_uri: `${window.location.protocol}//${window.location.hostname}:${window.location.port}/silent_renew.html`,
};

// create a user manager instance
export const userManager = createUserManager(config);

// create the middleware
export const oidcMiddleware = createOidcMiddleware(userManager);

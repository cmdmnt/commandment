export const JSONAPI_HEADERS = {
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json",
};

export const JSON_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
};

// TODO: This is for resource owner password grant but we should use something much more secure.
export const OAUTH2_CLIENT_ID = "F8955645-A21D-44AE-9387-42B0800ADF15";
export const OAUTH2_CLIENT_SECRET = "A";

// Flask-REST-JSONAPI Filter and Sort definitions

export interface OtherAction {
    type: string;
    payload?: any;
}

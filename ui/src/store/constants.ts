export const JSONAPI_HEADERS = {
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json",
};

export const JSON_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
};



// Flask-REST-JSONAPI Filter and Sort definitions

export interface OtherAction {
    type: string;
    payload?: any;
}

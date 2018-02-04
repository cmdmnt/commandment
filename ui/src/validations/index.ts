import {FieldValue, Validator} from "redux-form";

export const required: Validator = (value) => {
    return value ? undefined : "Required";
};

export const reverseDns: Validator = (value) => {
    if (!value) return undefined;
    if (value.slice(-1) === ".") { return "Should not end with a period"; }
    if (value.slice(0, 1) === ".") { return "Should not start with a period"; }
    return undefined;
};

export const httpsURL: Validator = (value: FieldValue) => value && !/^https:\/\//.test(value)
    ? "URL must begin with https://"
    : undefined;

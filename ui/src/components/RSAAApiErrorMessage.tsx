import * as React from "react";
import {ApiError} from "redux-api-middleware";
import Message from "semantic-ui-react/src/collections/Message/Message";
import {JSONAPIErrorObject, JSONAPIErrorResponse} from "../store/json-api";

export interface IRSAAApiErrorMessageProps {
    error: ApiError<JSONAPIErrorResponse>;
}

export const RSAAApiErrorMessage: React.FunctionComponent<IRSAAApiErrorMessageProps> =
    (props: IRSAAApiErrorMessageProps) => (
    <Message
        error
        header="An error occurred communicating with the server"
        list={[
            `Status: ${props.error.status} - ${props.error.statusText}`,
            ...props.error.response.errors.map((err: JSONAPIErrorObject) => `${err.detail}`),
        ]}
    />
);

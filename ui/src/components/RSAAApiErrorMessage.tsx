import * as React from "react";
import Message from "semantic-ui-react/src/collections/Message/Message";
import {ApiError} from "redux-api-middleware";

export interface IRSAAApiErrorMessageProps {
    error: ApiError;
}

export const RSAAApiErrorMessage: React.StatelessComponent<IRSAAApiErrorMessageProps> = (props, context) => (
    <Message
        error
        header="An error occurred communicating with the server"
        list={[
            `Status: ${props.error.status} - ${props.error.statusText}`
        ]}
    />
);

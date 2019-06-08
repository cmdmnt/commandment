import * as React from "react";
import {ApiError} from "redux-api-middleware";
import {Message} from "semantic-ui-react";

export interface IApiErrorProps {
    error: ApiError;
}

export const ApiError: React.FC = ({ error }: IApiErrorProps) => (
    <Message negative>
        <Message.Header>Unhandled API Error. This might be a bug</Message.Header>
        <p>{ error.response.code }</p>
    </Message>
);

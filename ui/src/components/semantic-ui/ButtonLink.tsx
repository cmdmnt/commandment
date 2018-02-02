import * as React from "react";
import {Link, Route} from "react-router-dom";
import Button, { ButtonProps } from "semantic-ui-react/src/elements/Button";

interface IButtonLinkProps extends ButtonProps {
    to: string;
}

/**
 * The ButtonLink component mixes the visual style and behaviour of a semantic-ui-react button with a react-router Link.
 * @param {IButtonLinkProps} props
 * @returns {any}
 * @constructor
 */
export const ButtonLink = (props: IButtonLinkProps) => (
    <Button as={Link} to={props.to} {...props} />
);

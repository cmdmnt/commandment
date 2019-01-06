import * as React from "react";
import Container from "semantic-ui-react/dist/commonjs/elements/Container/Container";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import Dropdown from "semantic-ui-react/dist/commonjs/modules/Dropdown/Dropdown";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";

export interface IAppStorePageProps {

}

export const AppStorePage: React.FunctionComponent<IAppStorePageProps> = (props: IAppStorePageProps) => {
    return (
        <Container>
            <Divider hidden />
            <Header as="h1">App Store</Header>

        </Container>
    );
};
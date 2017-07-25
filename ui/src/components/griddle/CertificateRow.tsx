import * as React from 'react';
import {connect} from 'react-redux';
import {components, plugins} from "griddle-react";
import {List, Button, Icon} from 'semantic-ui-react';
import {Store} from 'redux';
import {SyntheticEvent} from "react";

export interface CertificateRowProps extends components.RowProps {
    urlPrefix?: string;
    onClickButton: (e: any) => void;
}

export const CertificateRow = connect(
    (state: Store<any>, props: CertificateRowProps) => ({
        rowData: plugins.LocalPlugin.selectors.rowDataSelector(state, props),
        ...props
    })
)(({ rowData, onClickButton }) => (
    <List.Item>
        <List.Icon name={rowData.attributes.is_identity? 'id badge' : 'certificate'} size='large' verticalAlign="middle" />
        <List.Content>
            <List.Header>{rowData.attributes.x509_cn}</List.Header>
            <List.Description><Button size="tiny" onClick={onClickButton}><Icon name='download' /> PEM</Button></List.Description>
        </List.Content>
    </List.Item>
));

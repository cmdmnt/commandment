import * as React from 'react';
import {connect} from 'react-redux';
import {plugins} from "griddle-react";
import {List, Button, Icon} from 'semantic-ui-react';

export const CertificateRow = connect((state, props) => ({
    rowData: plugins.LocalPlugin.selectors.rowDataSelector(state, props)
}))(({ rowData }) => (
    <List.Item>
        <List.Icon name={rowData.attributes.is_identity? 'id badge' : 'certificate'} size='large' verticalAlign="middle" />
        <List.Content>
            <List.Header>{rowData.attributes.x509_cn}</List.Header>
            <List.Description></List.Description>
        </List.Content>
    </List.Item>
));

import {components, plugins} from "griddle-react";
import * as React from "react";
import {connect} from "react-redux";
import Icon from "semantic-ui-react/src/elements/Icon";
import List from "semantic-ui-react/src/elements/List";

import {Store} from "redux";

export interface CertificateRowProps extends components.RowProps {
    urlPrefix?: string;
    onClickButton: (e: any) => void;
}

export const CertificateRow = connect(
    (state: Store<any>, props: CertificateRowProps) => ({
        rowData: plugins.LocalPlugin.selectors.rowDataSelector(state, props),
        ...props,
    }),
)(({ rowData, onClickButton }) => (
    <List.Item>
        <List.Icon name={rowData.attributes.is_identity ? "id badge" : "certificate"} size="large" verticalAlign="middle" />
        <List.Content>
            <List.Header>{rowData.attributes.x509_cn}</List.Header>
            <List.Description><a className="button" href={`/api/v1/installed_certificates/${rowData.id}/download`}><Icon name="download" /> DER</a></List.Description>
        </List.Content>
    </List.Item>
));

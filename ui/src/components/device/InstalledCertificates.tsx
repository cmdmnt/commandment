import * as React from 'react';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {CertificateTypeIcon} from "../griddle/CertificateTypeIcon";

interface DeviceCertificatesProps {
    certificates: Array<JSONAPIObject<InstalledCertificate>>;
}


export class InstalledCertificates extends React.Component<DeviceCertificatesProps, undefined> {


    render() {
        const {
            certificates
        } = this.props;

        return (
            <Griddle
                data={certificates}
            >
                <RowDefinition>
                    <ColumnDefinition id="id" />
                    <ColumnDefinition title="Type" id="attributes.is_identity" customComponent={CertificateTypeIcon} />
                    <ColumnDefinition title="Common Name" id="attributes.x509_cn" />
                </RowDefinition>
            </Griddle>
        );
    }
}
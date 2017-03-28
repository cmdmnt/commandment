import * as React from 'react';
import {CERTIFICATE_PURPOSE} from "../constants";

interface CertificateDetailProps {
    certificate: Certificate;
}

export class CertificateDetail extends React.Component<CertificateDetailProps, undefined> {

    render() {
        const {
            certificate: {
                cert_type,
                subject,
                not_before,
                not_after,
                fingerprint
            }
        } = this.props;

        const description = CERTIFICATE_PURPOSE[cert_type];

        return (
            <div className='CertificateDetail'>
                <h3>{description}</h3>
                <dl>
                    <dt>Subject</dt>
                    <dd>{subject}</dd>

                    <dt>Not Before</dt>
                    <dd>{not_before}</dd>

                    <dt>Expires</dt>
                    <dd>{not_after}</dd>
                </dl>
            </div>
        )
    }
}
import * as React from 'react';
import {CERTIFICATE_PURPOSE} from "../constants";
import * as moment from 'moment';

import './CertificateDetail.scss';

interface CertificateDetailProps {
    certificate: JSONAPIDetailResponse<Certificate>;
    title: string;
}

export class CertificateDetail extends React.Component<CertificateDetailProps, undefined> {

    render() {
        const {
            certificate,
            title,
            children
        } = this.props;

        let content;
        let icon;
        let isValid = false;

        if (certificate) {
            const { subject, not_before, not_after } = this.props.certificate.data.attributes;

            const nowutc = moment().utc();
            
            const not_before_moment = moment(not_before);
            const not_after_moment = moment(not_after);

            const isExpired = nowutc.isAfter(not_after_moment);
            isValid = nowutc.isAfter(not_before_moment) && !isExpired;
            icon = isValid ? <i className='fa fa-id-card' /> : <i className='fa fa-warning' />;

            content = (
                <dl>
                    <dt>Subject</dt>
                    <dd>{subject}</dd>

                    <dt>From</dt>
                    <dd>{not_before_moment.fromNow()}</dd>

                    <dt>Expires</dt>
                    <dd className={`${isExpired ? 'warning' : ''}`}>{not_after_moment.fromNow()}</dd>
                </dl>
            )
        } else {
            icon = <i className='fa fa-question' />;
            content = <div>No certificate found</div>;
        }

        return (
            <div className='CertificateDetail paper padded'>
                <h3 className='centered'>{icon} {title}</h3>
                {content}
                {children}
            </div>
        )
    }
}
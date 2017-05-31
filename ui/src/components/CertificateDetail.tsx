import * as React from 'react';
import {CERTIFICATE_PURPOSE} from "../constants";
import * as moment from 'moment';

import './CertificateDetail.scss';
import {JSONAPIObject} from "../json-api";
import {Certificate} from "../models";

interface CertificateDetailProps {
    certificate: JSONAPIObject<Certificate>;
    title: string;
    onClickDelete: (certificateId: string) => void;
    onClickDownload: (certificateId: string) => void;
}

export class CertificateDetail extends React.Component<CertificateDetailProps, undefined> {

    handleClickDelete = (event: any): void => {
        this.props.onClickDelete(this.props.certificate.id);
    };

    handleClickDownload = (event: any): void => {
        event.preventDefault();
        this.props.onClickDownload(this.props.certificate.id);
    };

    render() {
        const {
            certificate,
            title,
            children
        } = this.props;

        let content;
        let icon;
        let isValid = false;

        if (certificate && certificate.attributes) {
            const { x509_cn, not_before, not_after } = certificate.attributes;

            const nowutc = moment().utc();
            
            const not_before_moment = moment(not_before);
            const not_after_moment = moment(not_after);

            const isExpired = nowutc.isAfter(not_after_moment);
            isValid = nowutc.isAfter(not_before_moment) && !isExpired;
            icon = isValid ? <i className='fa fa-id-card' /> : <i className='fa fa-warning' />;

            content = (
                <dl>
                    <dt>Common Name</dt>
                    <dd>{x509_cn}</dd>

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
                <button className='button button-outline float-right' onClick={this.handleClickDownload}>
                    <i className='fa fa-download' />
                </button>
                <h3>{title}</h3>

                {content}
                {children}
            </div>
        )
    }
}
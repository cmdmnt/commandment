import {isFuture, isPast, distanceInWordsToNow} from "date-fns";
import * as React from "react";
import {CERTIFICATE_PURPOSE} from "../../constants";

import {JSONAPIDataObject} from "../../json-api";
import {Certificate} from "../../store/certificates/types";
import "./CertificateDetail.scss";

interface CertificateDetailProps {
    certificate: JSONAPIDataObject<Certificate>;
    title: string;
    onClickDelete: (certificateId: string) => void;
    onClickDownload: (certificateId: string) => void;
}

export class CertificateDetail extends React.Component<CertificateDetailProps, undefined> {

    public handleClickDelete = (event: any): void => {
        this.props.onClickDelete("" + this.props.certificate.id);
    }

    public handleClickDownload = (event: any): void => {
        event.preventDefault();
        this.props.onClickDownload("" + this.props.certificate.id);
    }

    public render() {
        const {
            certificate,
            title,
            children,
        } = this.props;

        let content;
        let icon;
        let isValid = false;

        if (certificate && certificate.attributes) {
            const { x509_cn, not_before, not_after } = certificate.attributes;

            const isExpired = isPast(not_after);
            isValid = isFuture(not_before) && !isExpired;
            icon = isValid ? <i className="fa fa-id-card" /> : <i className="fa fa-warning" />;

            content = (
                <dl>
                    <dt>Common Name</dt>
                    <dd>{x509_cn}</dd>

                    <dt>From</dt>
                    <dd>{distanceInWordsToNow(not_before)}</dd>

                    <dt>Expires</dt>
                    <dd className={`${isExpired ? "warning" : ""}`}>{distanceInWordsToNow(not_after)}</dd>
                </dl>
            );
        } else {
            icon = <i className="fa fa-question" />;
            content = <div>No certificate found</div>;
        }

        return (
            <div className="CertificateDetail paper padded">
                <button className="button button-outline float-right" onClick={this.handleClickDownload}>
                    <i className="fa fa-download" />
                </button>
                <h3>{title}</h3>

                {content}
                {children}
            </div>
        );
    }
}

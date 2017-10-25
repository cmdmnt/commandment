import * as React from 'react';
import {Icon} from 'semantic-ui-react';

interface CertificateTypeIconProps {
    value: number;
    title: string;
}

export const CertificateTypeIcon: React.StatelessComponent<CertificateTypeIconProps> = (props: CertificateTypeIconProps): JSX.Element => {
    return <Icon name={props.value ? 'id badge': 'certificate'} />;
};
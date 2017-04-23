import * as React from 'react';

interface GriddleValue {
    griddleKey: number;
    value: any;
}

export const CertificateTypeIcon = (value: GriddleValue): JSX.Element => {
    // value.value = is_identity
    const iconClass = value.value ? 'fa fa-drivers-license-o' : 'fa fa-certificate';

    return <i className={iconClass} />;
};



export const CERTIFICATE_PURPOSE: {[propName: string]:string} = {
    'mdm.pushcert': 'APNS MDM Push Certificate',
    'mdm.webcrt': 'MDM Web Server Certificate',
    'mdm.cacert': 'MDM SCEP CA Certificate'
};

// Redux API Middleware Type Guards

export function isJSONAPIErrorResponsePayload(
    payload: JSONAPIListResponse<any> |
        JSONAPIDetailResponse<any> |
        JSONAPIErrorResponse): payload is JSONAPIErrorResponse {

    return (<JSONAPIErrorResponse>payload).errors !== undefined;
}
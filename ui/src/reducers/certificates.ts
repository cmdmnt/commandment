import * as actions from '../actions/certificates';


export interface CertificatesState {
    items: Array<any>;
    lastReceived?: Date;
}

const initialState: CertificatesState = {
    items: [],
    lastReceived: null
};

export function certificates(state: CertificatesState = initialState, action: any): CertificatesState {
    switch (action.type) {
        default:
            return state
    }
}
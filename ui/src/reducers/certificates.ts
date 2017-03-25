import * as actions from '../actions/certificates';


interface CertificatesState {
    items: Array<any>;
    lastReceived?: Date;
}

const initialState: CertificatesState = {
    items: [],
    lastReceived: null
};

export default function certificates(state: CertificatesState = initialState, action: any): CertificatesState {
    switch (action.type) {
        default:
            return state
    }
}
export interface SCEPState {

}

const initialState: SCEPState = {

};

export function scep(state: SCEPState = initialState, action: any): SCEPState {
    switch (action.type) {
        default:
            return state;
    }
}
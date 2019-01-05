import * as actions from './actions';
import {PostActionResponse} from "./actions";

export interface CommandsState {
    
}

const initialState: CommandsState = {
    
};

type CommandAction = PostActionResponse;

export function commands (state: CommandsState = initialState, action: CommandAction): CommandsState {
    switch (action.type) {
        default:
            return state;
    }
}

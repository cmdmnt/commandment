import * as actions from '../actions/commands';
import {PostActionResponse} from "../actions/commands";

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

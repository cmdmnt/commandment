import {combineReducers, Reducer} from 'redux';
import {account, IDEPAccountState} from "./account_reducer";
import {accounts, IDEPAccountsState} from "./accounts_reducer";
import {profiles, IDEPProfilesState} from "./profiles_reducer";
import {IDEPProfileState, profile} from "./profile_reducer";

export const dep = combineReducers({
    account,
    accounts,
    profile,
    profiles,
});

export interface IDEPState {
    account?: IDEPAccountState;
    accounts?: IDEPAccountsState;
    profiles?: IDEPProfilesState;
    profile?: IDEPProfileState;
}

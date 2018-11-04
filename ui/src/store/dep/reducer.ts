import {combineReducers, Reducer} from 'redux';
import {account, DEPAccountState} from "./account_reducer";
import {accounts, IDEPAccountsState} from "./accounts_reducer";
import {profiles, IDEPProfilesState} from "./profiles_reducer";
import {IDEPProfileState, profile} from "./profile_reducer";

export const dep = combineReducers({
    account,
    accounts,
    profiles,
    profile
});

export interface IDEPState {
    account?: DEPAccountState;
    accounts?: IDEPAccountsState;
    profiles?: IDEPProfilesState;
    profile?: IDEPProfileState;
}

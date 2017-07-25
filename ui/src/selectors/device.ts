import { createSelector, Selector as Reselector} from "reselect";
import {RootState} from "../reducers/index";

export const getDeviceAvailableCapacity = (state: RootState) => state.device.device ? state.device.device.attributes.available_device_capacity : null;
export const getDeviceCapacity = (state: RootState) => state.device.device ? state.device.device.attributes.device_capacity : null;

export const getPercentCapacityUsed: Reselector<RootState, number> = createSelector(
    [getDeviceCapacity, getDeviceAvailableCapacity],
    (deviceCapacity: number = 0, availableCapacity: number = 0) => (deviceCapacity - availableCapacity)
);


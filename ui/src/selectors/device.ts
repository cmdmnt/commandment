import { createSelector, Selector as Reselector} from "reselect";
import {IRootState} from "../reducers/index";

export const getDeviceAvailableCapacity = (state: IRootState) => state.device.device ? state.device.device.attributes.available_device_capacity : null;
export const getDeviceCapacity = (state: IRootState) => state.device.device ? state.device.device.attributes.device_capacity : null;

export const getPercentCapacityUsed: Reselector<IRootState, number> = createSelector(
    [getDeviceCapacity, getDeviceAvailableCapacity],
    (deviceCapacity: number = 0, availableCapacity: number = 0) => (deviceCapacity - availableCapacity)
);


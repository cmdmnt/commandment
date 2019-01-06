namespace MDM {
    export interface Command {
        RequestType: string;
    }

    export interface InstallProfile extends Command {
        Payload: any;
    }

    export interface RemoveProfile extends Command {
        Identifier: string;
    }

    export interface InstallProvisioningProfile extends Command {
        ProvisioningProfile: any;
    }

    export interface RemoveProvisioningProfile extends Command {
        Identifier: string;
    }

    export interface InstalledApplicationList extends Command {
        Identifiers?: Array<string>;
        ManagedAppsOnly?: boolean;
    }

    export interface DeviceInformation extends Command {
        Queries: Array<string>;
    }

    export interface DeviceLock extends Command {
        PIN: string;
        Message?: string;
        PhoneNumber?: string;
    }

    export interface ClearPasscode extends Command {
        UnlockToken: any;
    }

    export interface EraseDevice extends Command {
        PIN: string;
    }

    export interface RequestMirroring extends Command {
        DestinationName?: string;
        DestinationDeviceID?: string;
        ScanTime?: number;
        Password?: string;
    }

    export interface Restrictions extends Command {
        ProfileRestrictions?: boolean;
    }

    export interface DeleteUser extends Command {
        UserName: string;
        ForceDeletion?: boolean;
    }

    export interface InstallApplicationOptions {
        NotManaged: boolean;
        PurchaseMethod: number;
    }

    export interface InstallApplication extends Command {
        iTunesStoreID: number;
        Identifier?: string;
        Options?: InstallApplicationOptions;
        ManifestURL: string;
        ManagementFlags: number;
        Configuration?: any;
        Attributes?: any;
        ChangeManagementState?: 'Managed';
    }

    export interface ApplyRedemptionCode extends Command {
        Identifier: string;
        RedemptionCode: string;
    }

    export interface ManagedApplicationList extends Command {
        Identifiers?: Array<string>;
    }

    export interface RemoveApplication extends Command {
        Identifier: string;
    }

    export interface InviteToProgram extends Command {
        ProgramID: 'com.apple.cloudvpp';
        InvitationURL: string;
    }

    export interface ValidateApplications extends Command {
        Identifiers?: Array<string>;
    }
}

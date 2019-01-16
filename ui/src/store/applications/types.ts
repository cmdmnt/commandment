// valid relationship types
export type ApplicationRelationship = "tags";

export enum ApplicationDiscriminator {
    AppStoreMac = "appstore_mac",
    AppStoreIOS = "appstore_ios",
}

export interface Application {
    id?: string;
    itunes_store_id?: number;
    bundle_id?: string;
    purchase_method?: number;
    manifest_url: string;
    management_flags: number;
    change_management_state: "Managed" | null;
    display_name: string;
    description: string;
    version: string;

    country: string;
    artist_id: number;
    artist_name: string;
    artist_view_url: string;
    artwork_url60: string;
    artwork_url100: string;
    artwork_url512: string;
    release_notes: string;
    release_date: string;
    minimum_os_version: string;
    file_size_bytes: number;
}

export interface MacStoreApplication extends Application {
    discriminator: ApplicationDiscriminator.AppStoreMac;
}

export interface IOSStoreApplication extends Application {
    discriminator: ApplicationDiscriminator.AppStoreIOS;
}

export enum ManagedApplicationStatus {
    NeedsRedemption = "NeedsRedemption",
    Redeeming = "Redeeming",
    Prompting = "Prompting",
    PromptingForLogin = "PromptingForLogin",
    Installing = "Installing",
    ValidatingPurchase = "ValidatingPurchase",
    Managed = "Managed",
    ManagedButUninstalled = "ManagedButUninstalled",
    PromptingForUpdate = "PromptingForUpdate",
    PromptingForUpdateLogin = "PromptingForUpdateLogin",
    PromptingForManagement = "PromptingForManagement",
    Updating = "Updating",
    ValidatingUpdate = "ValidatingUpdate",
    Unknown = "Unknown",
    UserInstalledApp = "UserInstalledApp",
    UserRejected = "UserRejected",
    UpdateRejected = "UpdateRejected",
    ManagementRejected = "ManagementRejected",
    Failed = "Failed",
    Queued = "Queued",
}

export interface ManagedApplication {
    id: string;
    bundle_id: string;
    external_version_id?: number;
    has_configuration: boolean;
    has_feedback: boolean;
    is_validated: boolean;
    management_flags: number;
    status: ManagedApplicationStatus;
}

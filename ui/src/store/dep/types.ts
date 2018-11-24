
export enum DEPAccountOrgVersion {
    Version2 = "DEPOrgVersion.v2",
}

export enum DEPAccountOrgType {
    Education = "DEPOrgType.Education",
}

export enum SkipSetupSteps {
    AppleID = "AppleID",
    Biometric = "Biometric",
    Diagnostics = "Diagnostics",
    DisplayTone = "DisplayTone",
    Location = "Location",
    Passcode = "Passcode",
    Payment = "Payment",
    Privacy = "Privacy",
    Restore = "Restore",
    SIMSetup = "SIMSetup",
    Siri = "Siri",
    TOS = "TOS",
    Zoom = "Zoom",
    Android = "Android",
    HomeButtonSensitivity = "HomeButtonSensitivity",
    iMessageAndFaceTime = "iMessageAndFaceTime",
    OnBoarding = "OnBoarding",
    ScreenTime = "ScreenTime",
    SoftwareUpdate = "SoftwareUpdate",
    WatchMigration = "WatchMigration",
    Appearance = "Appearance",
    FileVault = "FileVault",
    iCloudDiagnostics = "iCloudDiagnostics",
    iCloudStorage = "iCloudStorage",
    Registration = "Registration",
    ScreenSaver = "ScreenSaver",
    TapToSetup = "TapToSetup",
    TVHomeScreenSync = "TVHomeScreenSync",
    TVProviderSignIn = "TVProviderSignIn",
    TVRoom = "TVRoom",
}

export interface DEPAccount {
    readonly access_token: string;
    readonly access_token_expiry: string;
    readonly admin_id: string;
    readonly consumer_key: string;
    readonly cursor?: string;
    readonly facilitator_id: string;
    readonly fetched_until?: string;
    readonly more_to_follow: boolean;
    readonly org_address: string;
    readonly org_email: string;
    readonly org_id: string;
    readonly org_id_hash: string;
    readonly org_name: string;
    readonly org_phone: string;
    readonly org_type: DEPAccountOrgType;
    readonly org_version: DEPAccountOrgVersion;
    readonly server_name: string;
    readonly server_uuid: string;
    readonly token_updated_at: string;
    readonly url?: string;
}

export interface DEPProfile {
    readonly id?: string;
    readonly uuid?: string;
    dep_account_id?: number;

    profile_name: string;
    url?: string;
    allow_pairing: boolean;
    is_supervised: boolean;
    is_multi_user: boolean;
    is_mandatory: boolean;
    await_device_configured: boolean;
    is_mdm_removable: boolean;
    support_phone_number: string;
    auto_advance_setup: boolean;
    support_email_address?: string;
    org_magic?: string;
    skip_setup_items: SkipSetupSteps[];
    department?: string;

    // anchor_certs
    // supervising_host_certs
}

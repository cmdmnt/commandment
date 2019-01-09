from enum import Enum


class ManagedAppStatus(Enum):
    """A list of possible Managed Application statuses returned by the `ManagedApplicationList` command."""
    NeedsRedemption = 'NeedsRedemption'
    Redeeming = 'Redeeming'
    Prompting = 'Prompting'
    PromptingForLogin = 'PromptingForLogin'
    Installing = 'Installing'
    ValidatingPurchase = 'ValidatingPurchase'
    Managed = 'Managed'
    ManagedButUninstalled = 'ManagedButUninstalled'
    PromptingForUpdate = 'PromptingForUpdate'
    PromptingForUpdateLogin = 'PromptingForUpdateLogin'
    PromptingForManagement = 'PromptingForManagement'
    Updating = 'Updating'
    ValidatingUpdate = 'ValidatingUpdate'
    Unknown = 'Unknown'

    # Transient
    UserInstalledApp = 'UserInstalledApp'
    UserRejected = 'UserRejected'
    UpdateRejected = 'UpdateRejected'
    ManagementRejected = 'ManagementRejected'
    Failed = 'Failed'

    # Commandment ONLY - To indicate that the command for IA is queued but not yet acked
    Queued = 'Queued'

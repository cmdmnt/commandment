# Flask Dev Server
PORT = 5443

# Flask-Alembic imports configuration from here instead of the alembic.ini
ALEMBIC = {
    'script_location': '%(here)s/alembic/versions'
}

ALEMBIC_CONTEXT = {
    'render_as_batch': True,  # Necessary to support SQLite ALTER on constraints
}

# http://flask-sqlalchemy.pocoo.org/2.1/config/
SQLALCHEMY_DATABASE_URI = 'sqlite:///commandment/commandment.db'
# FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.
SQLALCHEMY_TRACK_MODIFICATIONS = False


# PLEASE! Do not take this key and use it for another product/project. It's
# only for Commandment's use. If you'd like to get your own (free!) key
# contact the mdmcert.download administrators and get your own key for your
# own project/product.  We're trying to keep statistics on which products are
# requesting certs (per Apple T&C). Don't force Apple's hand and
# ruin it for everyone!
MDMCERT_API_KEY = 'b742461ff981756ca3f924f02db5a12e1f6639a9109db047ead1814aafc058dd'

PLISTIFY_MIMETYPE = 'application/xml'


# Internal CA - Certificate X.509 Attributes
INTERNAL_CA_CN = 'COMMANDMENT-CA'
INTERNAL_CA_O = 'Commandment'


# --------------
# SCEPy Defaults
# --------------

# Directory where certs, revocation lists, serials etc will be kept
SCEPY_CA_ROOT = "CA"

# X.509 Name Attributes used to generate the CA Certificate
SCEPY_CA_X509_CN = 'SCEPY-CA'
SCEPY_CA_X509_O = 'SCEPy'
SCEPY_CA_X509_C = 'US'

# Force a single certificate to be returned as a PKCS#7 Degenerate instead of raw DER data
SCEPY_FORCE_DEGENERATE_FOR_SINGLE_CERT = False


# These applications will not be shown in inventory.
IGNORED_APPLICATION_BUNDLE_IDS = [
    'com.apple.MigrateAssistant',
    'com.apple.keychainaccess',
    'com.apple.grapher',
    'com.apple.Grab',
    'com.apple.ActivityMonitor',
    'com.apple.backup.launcher',  # Time Machine
    'com.apple.TextEdit',
    'com.apple.systempreferences',
    'com.apple.CoreLocationAgent',
    'com.apple.CaptiveNetworkAssistant',
    'com.apple.CalendarFileHandler',
    'com.apple.BluetoothUIServer',
    'com.apple.BluetoothSetupAssistant',
    'com.apple.AutomatorRunner',
    'com.apple.AppleFileServer',
    'com.apple.AirportBaseStationAgent',
    'com.apple.AirPlayUIAgent',
    'com.apple.AddressBook.UrlForwarder',
    'com.apple.AVB-Audio-Configuration',
    'com.apple.ScriptMonitor',
    'com.apple.ScreenSaver.Engine',
    'com.apple.systemevents',
    'com.apple.stocks',
    'com.apple.Spotlight',
    'com.apple.SoftwareUpdate',
    'com.apple.SocialPushAgent',
    'com.apple.Siri',
    'com.apple.screencapturetb',
    'com.apple.rcd',
    'com.apple.CloudKit.ShareBear',
    'com.apple.cloudphotosd',
    'com.apple.wifi.WiFiAgent',
    'com.apple.weather',
    'com.apple.VoiceOver',
    'com.apple.UserNotificationCenter',
    'com.apple.UnmountAssistantAgent',
    'com.apple.UniversalAccessControl',
    'com.apple.Ticket-Viewer',
    'com.apple.ThermalTrap',
    'com.apple.systemuiserver',
    'com.apple.check_afp',
    'com.apple.AddressBook.sync',
    'com.apple.AddressBookSourceSync',
    'com.apple.AddressBook.abd',
    'com.apple.ABAssistantService',
    'com.apple.FontRegistryUIAgent',
    'com.apple.speech.synthesis.SpeechSynthesisServer',
    'com.apple.print.PrinterProxy',
    'com.apple.StorageManagementLauncher',
    'com.apple.Terminal',
    'com.apple.PhotoBooth',
    'com.apple.mail',
    'com.apple.notificationcenter.widgetsimulator',
    'com.apple.quicklook.ui.helper',
    'com.apple.quicklook.QuickLookSimulator',
    'com.apple.QuickLookDaemon32',
    'com.apple.QuickLookDaemon',
    'com.apple.syncserver',
    'com.apple.WebKit.PluginHost',
    'com.apple.AirScanScanner',
    'com.apple.MakePDF',
    'com.apple.BuildWebPage',
    'com.apple.VIM-Container',
    'com.apple.TrackpadIM-Container',
    'com.apple.inputmethod.Tamil',
    'com.apple.TCIM-Container',
    'com.apple.exposelauncher',
    'com.apple.iChat',
    'com.apple.Maps',
    'com.apple.launchpad.launcher',
    'com.apple.FaceTime',
    'com.apple.Dictionary',
    'com.apple.dashboardlauncher',
    'com.apple.DVDPlayer',
    'com.apple.Chess',
    'com.apple.iCal',
    'com.apple.calculator',
    'com.apple.Automator',
    'com.apple.KIM-Container',
    'com.apple.CharacterPaletteIM',
    'com.apple.inputmethod.AssistiveControl',
    'com.apple.VirtualScanner',
    'com.apple.Type8Camera',
    'com.apple.loginwindow',
    'com.apple.SetupAssistant',
    'com.apple.PhotoLibraryMigrationUtility',
    'com.apple.notificationcenterui',
    'com.apple.ManagedClient',
    'com.apple.helpviewer',
    'com.apple.finder.Open-iCloudDrive',
    'com.apple.finder.Open-Recents',
    'com.apple.finder.Open-Network',
    'com.apple.finder.Open-Computer',
    'com.apple.finder.Open-AllMyFiles',
    'com.apple.finder.Open-AirDrop',
    'com.apple.finder',
    'com.apple.dock',
    'com.apple.coreservices.uiagent',
    'com.apple.controlstrip',
    'com.apple.CertificateAssistant',
    'com.apple.wifi.diagnostics',
    'com.apple.SystemImageUtility',
    'com.apple.RAIDUtility',
    'com.apple.NetworkUtility',
    'com.apple.FolderActionsSetup',
    'com.apple.DirectoryUtility',
    'com.apple.AboutThisMacLauncher',
    'com.apple.AppleScriptUtility',
    'com.apple.AppleGraphicsWarning',
    'com.apple.print.add',
    'com.apple.archiveutility',
    'com.apple.appstore',
    'com.apple.Console',
    'com.apple.bootcampassistant',
    'com.apple.BluetoothFileExchange',
    'com.apple.siri.launcher',
    'com.apple.reminders',
    'com.apple.QuickTimePlayerX',
    'com.apple.Image_Capture',
    'com.apple.accessibility.universalAccessAuthWarn',
    'com.apple.accessibility.universalAccessHUD',
    'com.apple.accessibility.DFRHUD',
    'com.apple.syncservices.syncuid',
    'com.apple.syncservices.ConflictResolver',
    'com.apple.STMFramework.UIHelper',
    'com.apple.speech.SpeechRecognitionServer',
    'com.apple.speech.SpeechDataInstallerd',
    'com.apple.ScreenReaderUIServer',
    'com.apple.PubSubAgent',
    'com.apple.nbagent',
    'com.apple.soagent',
    'com.apple.imtransferservices.IMTransferAgent',
    'com.apple.IMAutomaticHistoryDeletionAgent',
    'com.apple.imagent',
    'com.apple.imavagent',
    'com.apple.idsfoundation.IDSRemoteURLConnectionAgent',
    'com.apple.identityservicesd',
    'com.apple.FindMyMacMessenger',
    'com.apple.Family',
    'com.apple.familycontrols.useragent',
    'com.apple.eap8021x.eaptlstrust',
    'com.apple.frameworks.diskimages.diuiagent',
    'com.apple.FollowUpUI',
    'com.apple.CCE.CIMFindInputCode',
    'com.apple.cmfsyncagent',
    'com.apple.storeuid',
    'com.apple.lateragent',
    'com.apple.bird',  # iCloud Drive
    'com.apple.AskPermissionUI',
    'com.apple.Calibration-Assistant',
    'com.apple.AccessibilityVisualsAgent',
    'com.apple.AOSPushRelay',
    'com.apple.AOSHeartbeat',
    'com.apple.AOSAlertManager',
    'com.apple.iCloudUserNotificationsd',
    'com.apple.SCIM-Container',
    'com.apple.PAH-Container',
    'com.apple.inputmethod.PluginIM',
    'com.apple.KeyboardViewer',
    'com.apple.PIPAgent',
    'com.apple.OSDUIHelper',
    'com.apple.ODSAgent',
    'com.apple.OBEXAgent',
    'com.apple..NowPlayingWidgetContainer',
    'com.apple.NowPlayingTouchUI',
    'com.apple.NetAuthAgent',
    'com.apple.MemorySlotUtility',
    'com.apple.locationmenu',
    'com.apple.Language-Chooser',
    'com.apple.security.Keychain-Circle-Notification',
    'com.apple.KeyboardSetupAssistant',
    'com.apple.JavaWebStart',
    'com.apple.JarLauncher',
    'com.apple.Installer-Progress',
    'com.apple.PackageKit.Install-in-Progress',
    'com.apple.dt.CommandLineTools.installondemand',
    'com.apple.imageevents',
    'com.apple.gamecenter',
    'com.apple.FolderActionsDispatcher',
    'com.apple.ExpansionSlotUtility',
    'com.apple.EscrowSecurityAlert',
    'com.apple.DwellControl',
    'com.apple.DiscHelper',
    'com.apple.databaseevents',
    'com.apple.ColorSyncCalibrator',
    'com.apple.print.AirScanLegacyDiscovery',
    'com.apple.ScriptEditor.id.image-file-processing-droplet-template',
    'com.apple.ScriptEditor.id.file-processing-droplet-template',
    'com.apple.ScriptEditor.id.droplet-with-settable-properties-template',
    'com.apple.ScriptEditor.id.cocoa-applet-template',
    'com.apple.inputmethod.Ainu',
    'com.apple.50onPaletteIM',
    'com.apple.AutoImporter',
    'com.apple.Type5Camera',
    'com.apple.Type4Camera',
    'com.apple.PTPCamera',
    'com.apple.MassStorageCamera',
    'com.apple.imautomatichistorydeletionagent',
    'com.apple.SyncServices.AppleMobileSync',
    'com.apple.SyncServices.AppleMobileDeviceHelper',
    'com.apple.coreservices.UASharedPasteboardProgressUI',
    'com.apple.SummaryService',
    'com.apple.ImageCaptureService',
    'com.apple.ChineseTextConverterService',
    'com.apple.Pass-Viewer',
    'com.apple.PowerChime',
    'com.apple.ProblemReporter',
    'com.apple.pluginIM.pluginIMRegistrator',
    'com.apple.ReportPanic',
    'com.apple.RemoteDesktopAgent',
    'com.apple.RapportUIAgent',
    'com.apple.MRT',
    'com.apple.AirPortBaseStationAgent',
    'com.apple.appstore.AppDownloadLauncher',
    'com.apple.appleseed.FeedbackAssistant',
    'com.apple.ScreenSharing',
    'com.apple.FirmwareUpdateHelper',
    'com.apple.SecurityFixer',
    'com.apple.ZoomWindow.app',
    'com.apple.IMServicePlugInAgent',
    'com.apple.itunes.connect.ApplicationLoader',
    'com.apple.DiskImageMounter',
]

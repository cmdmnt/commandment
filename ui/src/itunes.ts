
export interface IiTunesSearchResult {
    resultCount: number;
    results: IiTunesSoftwareSearchResult[];
}

export interface IiTunesSoftwareSearchResult {
    isGameCenterEnabled: boolean;
    ipadScreenshotUrls: string[];
    screenshotUrls: string[];
    appletvScreenshotUrls: string[];
    artworkUrl60: string;
    artworkUrl512: string;
    artworkUrl100: string;
    artistViewUrl: string;
    advisories: string[];
    supportedDevices: string[];
    kind: string;
    features: string[];
    trackCensoredName: string;
    languageCodesISO2A: string[];
    fileSizeBytes: number;
    sellerUrl: string;
    contentAdvisoryRating: string;
    trackViewUrl: string;
    trackContentRating: string;
    releaseNotes: string;
    formattedPrice: string;
    trackName: string;
    primaryGenreName: string;
    genreIds: string[];
    sellerName: string;
    releaseDate: string;  // eg 2016-11-04T19:34:13Z
    primaryGenreId: number;
    isVppDeviceBasedLicensingEnabled: boolean;
    currency: string;
    wrapperType: string;
    version: string;
    trackId: number;
    description: string;
    artistId: number;
    artistName: string;
    genres: string[];
    price: number;
    minimumOsVersion: string;
    bundleId: string;
    currentVersionReleaseDate: string;
    averageUserRating: number;
    userRatingCount: number;
}

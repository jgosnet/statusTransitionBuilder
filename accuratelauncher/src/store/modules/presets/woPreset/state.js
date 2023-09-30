export default {
  presetName: "Accurate_WO",
  woMetadata: {},
  providerData: "",
  outputStatuses: {
    "0": {
      key: "Pass",
      color: "var(--AP-SUCCESS)",
      index: 0
    },
    "1": {
      key: "Fail",
      color: "var(--AP-ERROR)",
      index: 1
    }
  },
  statusIndex: 2,
  possibleStatusColors: ['var(--AP-SUCCESS)', 'var(--AP-ERROR)', 'var(--AP-FOREGROUND-2)'],
  metadataFields: {},
  metadataIndex: 0,
  possibleMetadataSources: ['metadata', 'properties'],
  possibleDisplayTypes: ['smpte', 'date','time','date-time'],
  possibleStoredTypes: ['timebase', 'utcDate'],

  possibleProperties: [
    {
      key: 'duration',
      label: 'Duration',
      storedType: 'timebase',
      displayType: 'smpte'
    },
    {
      key: 'resolution',
      label: 'Resolution'
    },
    {
      key: 'frameRate',
      label: 'Frame Rate'
    },
    {
      key: 'aspectRatio',
      label: 'Aspect Ratio'
    },
    {
      key: 'bitrate',
      label: 'Bitrate'
    },
    {
      key: 'codec',
      label: 'Codec'
    },
    {
      key: 'creationDate',
      label: 'Creation Date',
      storedType: 'date-time',
      displayType: 'utcDate'
    },
    {
      key: 'updateDate',
      label: 'Updated',
      storedType: 'date-time',
      displayType: 'utcDate'
    }
  ],

  defaultOutputSpecs: {
    avQcManual: {
      index: "avQcManual",
      regexp: "avQcManual",
      label: "acc_manual_tbmd",
      location: "Artifacts",
      name: "accurate_material/<assetName>_acc_manual_tbmd.json"
    },
    avQcStatus: {
      index: "avQcStatus",
      regexp: "avQcStatus",
      label: "acc_qc_status",
      location: "Artifacts",
      name: "accurate_material/<assetName>_acc_qc_status.json"
    },
    avAssetMetadataExport: {
      index: "avAssetMetadataExport",
      regexp: "avAssetMetadataExport",
      label: "acc_metadata_export",
      location: "Artifacts",
      name: "accurate_material/<assetName>_acc_metadata_export.json"
    }
  },
  outputSpecs: {},
  outputSpecsIndex: 0,
  metadataViewAsset: {
    asset: {
      name: "asset",
      readOnlyFields: [],
    },
    videoFile: {
      name: "videoFile",
      readOnlyFields: [],
    },
    videoStream: {
      name: "videoStream",
      readOnlyFields: [],
    },
    audioFile: {
      name: "audioFile",
      readOnlyFields: [],
    },
    audioStream: {
      name: "audioStream",
      readOnlyFields: [],
    },
  },

  defaultManualMarkers: {
    videoIssues: {
      "index": "videoIssues",
      "track": "videoIssues",
      "title": "Video Errors",
      "backgroundColor": "#FFFF00",
      "hoverColor": "#0000FF"
    },
    audioIssues: {
      "index": "audioIssues",
      "track": "audioIssues",
      "title": "Audio Errors",
      "backgroundColor": "#FFA500",
      "hoverColor": "#0000FF"
    },
    ccIssues: {
      "index": "ccIssues",
      "track": "ccIssues",
      "title": "Closed Caption Errors",
      "backgroundColor": "#ff0000",
      "hoverColor": "#0000FF"
    }
  },
  manualMarkers: {},
  manualMarkersIndex: 0,

  forms: {},
  formIndex: 0,
}
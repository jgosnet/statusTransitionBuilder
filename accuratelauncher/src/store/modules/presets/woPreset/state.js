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
  possibleMetadataSources: ['metadata', 'property'],
  possibleDisplayTypes: ['smpte', 'date','time','date-time'],
  possibleStoredTypes: ['timebase', 'utcDate'],

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
  }
}
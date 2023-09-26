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

}
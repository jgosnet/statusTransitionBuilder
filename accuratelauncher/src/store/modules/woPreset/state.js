export default {
  presetName: "Accurate_WO",
  woMetadata: {},
  outputStatuses: {
    "0": {
      "key": "Pass",
      "labels": {
        "status": "Pass",
        "assign": "Pass"
      },
      "color": "var(--AP-SUCCESS)",
      "allowComment": true
    },
    "1": {
      "key": "Fail",
      "labels": {
        "status": "Fail",
        "assign": "Fail"
      },
      "color": "var(--AP-ERROR)",
      "allowComment": true
    }
  },
  statusIndex: 2,
}
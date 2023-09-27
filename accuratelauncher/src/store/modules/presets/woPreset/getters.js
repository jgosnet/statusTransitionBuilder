export default {
  // eslint-disable-next-line no-unused-vars
  woProviderData(state, getters, rootState, rootGetters){
    console.log("display wo provider data")

    let res = {
      gateway: {
        players: {
          video: ""
        }
      },
      services: {
        accuratePlayer: {
          avFrontend: {
            settings: {
              forms: {
                assetForm: {
                  schema: {
                    type: "object",
                    properties: {
                    }
                  },
                  uischema: {
                    type: "VerticalLayout",
                    elements: []
                  }
                }
              },
              assetStatus: {
                statusMetadataFieldName: "asset_status",
                commentMetadataFieldName: "asset_status_comment",
                statusSetByMetadataFieldName: "asset_status_set_by",
                statuses: getters['formattedOutputStatus']
              },
              metadataFields: getters['formattedMetadataFields'],
              metadataViews: [
              ],
              manualMarkerTracks: [
              ]
            }
          }
        }
      }
    };
    let resString = JSON.stringify(res, null, 2);
    resString = resString.replace('"video": ""', '"video": {{DYNAMIC_PRESET_DATA[\'video_data\'] | tojson | replace(\'\\u003c\', \'<\') | replace(\'\\u003e\', \'>\')}}')
    return resString
  },
  // eslint-disable-next-line no-unused-vars
  woRallyConfig(state, getters, rootState, rootGetters){
    console.log("display wo rallyconfig")
    let res = {
      PresetName: "builder_wo",
      inputSpec: "{{DYNAMIC_PRESET_DATA['input_specs'] | tojson}}",
      outputSpec: getters['formattedOutputSpecs']
    };
    return JSON.stringify(res, null, 4)
  },
  outputStatuses(state){
    return state.outputStatuses
  },
  formattedOutputStatus(state){
    let jsonAssetStatuses = []
    for (let itemIndex in state.outputStatuses){
      const assetStatusItem = state.outputStatuses[itemIndex]
      jsonAssetStatuses.push({
        key: assetStatusItem.key,
        labels: {
          status: assetStatusItem.key,
          assign: assetStatusItem.key
        },
        color: assetStatusItem.color,
        allowComment: true
      })
    }
    return jsonAssetStatuses;
  },
  possibleStatusColors(state){
    return state.possibleStatusColors
  },
  metadataFields(state){
    return state.metadataFields
  },
  formattedMetadataFields(state){
    let jsonMdFields = []
    for (let itemIndex in state.metadataFields){
      const mdFieldItem = state.metadataFields[itemIndex]
      jsonMdFields.push({
        id: mdFieldItem.index + mdFieldItem.key,
        key: mdFieldItem.key,
        label: mdFieldItem.displayName,
        source: mdFieldItem.source,
        displayType: mdFieldItem.displayType,
        storedType: mdFieldItem.storedType,
      })
    }
    return jsonMdFields;
  },
  possibleMetadataSources(state){
    return state.possibleMetadataSources
  },
  possibleDisplayTypes(state){
    return state.possibleDisplayTypes
  },
  possibleStoredTypes(state){
    return state.possibleStoredTypes
  },
  outputSpecs(state){
    return state.outputSpecs
  },
  formattedOutputSpecs(state){
    let jsonOutputSpecs = {}
    for (let itemIndex in state.outputSpecs){
      const item = state.outputSpecs[itemIndex]
      jsonOutputSpecs[item.regexp] = {
        label: item.label,
        location: item.location,
        name: item.name
      }
    }
    return jsonOutputSpecs;
  },
  metadataViewAsset(state){
    return state.metadataViewAsset;
  },
}
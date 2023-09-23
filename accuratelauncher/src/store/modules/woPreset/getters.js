export default {
  // eslint-disable-next-line no-unused-vars
  woProviderData(state, getters, rootState, rootGetters){
    console.log("display wo provider data")
    //
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
                statuses: [
                  {
                    key: "Pass",
                    labels: {
                      status: "Pass",
                      assign: "Pass"
                    },
                    color: "var(--AP-SUCCESS)",
                    allowComment: true
                  },
                  {
                    key: "Fail",
                    labels: {
                      status: "Fail",
                      assign: "Fail"
                    },
                    color: "var(--AP-ERROR)",
                    allowComment: true
                  }
                ]
              },
              metadataFields: [],
              metadataViews: [
              ],
              manualMarkerTracks: [
              ]
            }
          }
        }
      }
    };
    let resString = JSON.stringify(res, null, 2)
    // resString = resString.replace('"video": ""', '"video": {{DYNAMIC_PRESET_DATA[\'video_data\'] | tojson | replace(\'\\u003c\', \'<\') | replace(\'\\u003e\', \'>\')}}')
    return resString
  },
  // eslint-disable-next-line no-unused-vars
  woRallyConfig(state, getters, rootState, rootGetters){
    console.log("display wo provider data")
    let res = {};
    return JSON.stringify(res, null, 4)
  },
}
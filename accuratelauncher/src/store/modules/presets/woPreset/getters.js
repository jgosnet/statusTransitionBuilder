export default {
  // eslint-disable-next-line no-unused-vars
  woProviderData(state, getters, rootState, rootGetters){
    console.log("display wo provider data")

    let res = {
      gateway: {
        players: ""
      },
      services: {
        accuratePlayer: {
          avFrontend: {
            settings: {
              forms: getters['formattedForms'],
              assetStatus: {
                statusMetadataFieldName: "asset_status",
                commentMetadataFieldName: "asset_status_comment",
                statusSetByMetadataFieldName: "asset_status_set_by",
                statuses: getters['formattedOutputStatus']
              },
              metadataFields: getters['formattedMetadataFields'],
              metadataViews: [
                getters['formattedMetadataViewAsset']
              ],
              manualMarkerTracks: getters['formattedManualMarkers']
            }
          }
        }
      }
    };
    let resString = JSON.stringify(res, null, 2);
    resString = resString.replace('"players": ""', '"players": {{DYNAMIC_PRESET_DATA[\'video_data\'] | tojson | replace(\'\\\\u003c\', \'<\') | replace(\'\\\\u003e\', \'>\')}}')
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
  editableMetadataFieldLabels(state){
    let jsonMdFields = []
    for (let itemIndex in state.metadataFields){
      const mdFieldItem = state.metadataFields[itemIndex]
      if (mdFieldItem.source === 'metadata'){
        jsonMdFields.push(mdFieldItem.displayName)
      }

    }
    return jsonMdFields;
  },
  metadataFields(state){
    return state.metadataFields
  },
  formattedMetadataFields(state){
    let jsonMdFields = []
    for (let itemIndex in state.metadataFields){
      const mdFieldItem = state.metadataFields[itemIndex]
      jsonMdFields.push({
        id: mdFieldItem.index + '_' + mdFieldItem.key,
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
  possibleProperties(state){
    return state.possibleProperties
  },
  possiblePropertiesNames(state){
    return state.possibleProperties.map(obj => obj.key)
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
  // eslint-disable-next-line no-unused-vars
  formattedMetadataViewAsset(state){
    let assetReadonlyFields = state.metadataViewAsset.asset.readOnlyFields.map(obj =>{
      return {
        metadataFieldId: obj.index + '_' + obj.key
      };
    })
    let videoStreamReadonlyFields = state.metadataViewAsset.videoStream.readOnlyFields.map(obj =>{
      return {
        metadataFieldId: obj.index + '_' + obj.key
      };
    })
    let audioStreamReadonlyFields = state.metadataViewAsset.audioStream.readOnlyFields.map(obj =>{
      return {
        metadataFieldId: obj.index + '_' + obj.key
      };
    })
    let videoFileReadonlyFields = state.metadataViewAsset.videoFile.readOnlyFields.map(obj =>{
      return {
        metadataFieldId: obj.index + '_' + obj.key
      };
    })
    let audioFileReadonlyFields = state.metadataViewAsset.audioFile.readOnlyFields.map(obj =>{
      return {
        metadataFieldId: obj.index + '_' + obj.key
      };
    })



    console.log("assetReadonlyFields")
    console.log(assetReadonlyFields)

    let res = {
      active: true,
      id: "defaultMetadataView",
      name: "Default",
      description: "The default metadata view",
      fieldSets: {
        asset: {
          form: state.metadataViewAsset.asset.form,
          readOnlyFields: assetReadonlyFields,
        },
        videoStream: {
          readOnlyFields: videoStreamReadonlyFields,
        },
        audioStream: {
          readOnlyFields: audioStreamReadonlyFields,
        },
        videoFile: {
          readOnlyFields: videoFileReadonlyFields,
        },
        audioFile: {
          readOnlyFields: audioFileReadonlyFields,
        }
      }
    }

    return res;
  },
  manualMarkers(state){
    return state.manualMarkers
  },
  formattedManualMarkers(state){
    let arrayMarkers = []
    let index = 1;
    for (let itemIndex in state.manualMarkers){
      const markerItem = state.manualMarkers[itemIndex]
      arrayMarkers.push({
        track: markerItem.track,
        title: markerItem.title,
        form: markerItem.associatedForm,
        order: index,
        markerStyle: {
          backgroundColor: markerItem.backgroundColor,
          hover: {
            backgroundColor: markerItem.hoverColor
          }
        },

      })
      index += 1;
    }
    return arrayMarkers;
  },
  forms(state){
    return state.forms
  },
  formsNames(state){
    let arrayForms = []
    for (let itemIndex in state.forms){
      const formItem = state.forms[itemIndex]
      arrayForms.push(formItem.name)
    }
    return arrayForms;
  },
  formattedForms(state, getters){
    let dictForms = {}
    for (let itemIndex in state.forms){
      const formItem = state.forms[itemIndex];

      let formSchema =
        {
          schema: {
            type: "object",
            properties: {},
            required: [],
          },
          uischema: {
            type: "VerticalLayout",
            elements: [],
            defaultValues: {
            }
          }
        }

      formItem.properties.forEach( elt => {
        const associatedMdObj = getters['formattedMetadataFields'].find(obj => obj.label === elt.associatedMetadata)

        if (associatedMdObj){
          if (elt.isRequired){
            formSchema['schema']['required'].push(associatedMdObj.key);
          }
          formSchema['schema']['properties'][associatedMdObj.key] = {
            type: elt.fieldType,
          }
          if (elt.displayType === 'radiobutton' ||
              elt.displayType === 'checkbox' ||
                !elt.displayType){
            if (elt.hasEnum){
              if (elt.fieldType === 'string'){
                formSchema['schema']['properties'][associatedMdObj.key]['enum'] = elt.enumList.map(enumVal => enumVal.name);
              } else if (elt.fieldType === 'array'){
                formSchema['schema']['properties'][associatedMdObj.key]['items']= {enum: elt.enumList.map(enumVal => enumVal.name)};
              }

            }
          }

          if (elt.defaultValue){
            formSchema['uischema']['defaultValues'][associatedMdObj.key] = elt.defaultValue;
          }

          let uiDict = {
            type: "Control",
            scope: `#/properties/${associatedMdObj.key}`,
            options: {}
          }
          if (elt.displayType === 'radiobutton'){
            uiDict['options']['format'] = 'radio';
          }
          if (elt.displayType === 'checkbox'){
            uiDict['options']['format'] = 'checkbox';
          }
          if (elt.displayType === 'date'){
            uiDict['options']['format'] = 'date';
          }
          if (elt.fieldType === 'boolean' || elt.displayType === 'boolean'){
            uiDict['options']['toggle'] = true;
          }

          formSchema['uischema']['elements'].push(uiDict)
        }


      });

      dictForms[formItem.name] = formSchema;
    }
    return dictForms;
  },
}
export default {
  updateProviderData(state, value){
    state.providerData = value
  },
  addOutputStatus(state){
    state.outputStatuses[state.statusIndex] = {
      key: "New",
      color: "var(--AP-SUCCESS)",
      index: state.statusIndex
    };
    state.statusIndex += 1;
  },
  deleteOutputStatus(state, item){
    console.log(`trying to delete: ${item.index}`)
    console.log(item)
    delete state.outputStatuses[item.index];
    for (const index in state.outputStatuses){
      console.log(state.outputStatuses[index])
    }
  },
  addMetadataField(state, payload){
    console.log("payload")
    console.log(payload)
    state.metadataFields[state.metadataIndex] = {
      key: payload.key,
      index: state.metadataIndex,
      source: payload.source,
      displayName: payload.displayName,
      storedType: payload.storedType,
      displayType: payload.displayType,
      isExpanded: true,
      autoPopulate: payload.autoPopulate,
      jmespath: payload.jmespath,
    };
    if (payload.source === 'properties'){
      state.metadataFields[state.metadataIndex]['isExpanded'] = false
    }
    state.metadataIndex += 1;
  },
  deleteMetadataField(state, item){
    console.log(`trying to delete: ${item.index}`)
    console.log(item)
    delete state.metadataFields[item.index];
    for (const index in state.metadataFields){
      console.log(state.metadataFields[index])
    }
  },
  addOutputSpec(state){
    state.outputSpecs[state.outputSpecsIndex] = {
      index: state.outputSpecsIndex,
      regexp: "",
      label: "",
      location: "",
      name: "<assetName>"
    };
    state.outputSpecsIndex += 1;
  },
  deleteOutputSpec(state, item){
    console.log(`trying to delete: ${item.index}`)
    console.log(item)
    delete state.outputSpecs[item.index];
    for (const index in state.outputSpecs){
      console.log(state.outputSpecs[index])
    }
  },
  resetOutputSpecs(state){
    state.outputSpecs = {...state.defaultOutputSpecs};
    state.outputSpecsIndex = 0;
  },
  resetManualMarkers(state){
    state.manualMarkers = {...state.defaultManualMarkers};
    state.manualMarkersIndex = 0;
  },
  deleteManualMarker(state, item){
    console.log(`trying to delete: ${item.index}`)
    console.log(item)
    delete state.manualMarkers[item.index];
  },
  addManualMarker(state) {
    state.manualMarkers[state.manualMarkersIndex] = {
      index: state.manualMarkersIndex,
      track: "track-" + state.manualMarkersIndex,
      title: "",
      backgroundColor: "#008000",
      hoverColor: "#0000FF",
      isExpanded: true,
      associatedForm: "",
    };
    state.manualMarkersIndex += 1;
  },
  addForm(state) {
    state.forms[state.formIndex] = {
      index: state.formIndex,
      name: "customForm" + state.formIndex,
      properties: [],
      isExpanded: true
    };
    state.formIndex += 1;
  },
  deleteForm(state, item){
    console.log(`trying to delete: ${item.index}`)
    console.log(item)
    delete state.forms[item.index];
  },
}
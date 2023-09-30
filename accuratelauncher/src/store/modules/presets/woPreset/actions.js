export default {
  updateProviderData(context, value){
    context.commit('updateProviderData', value)
  },
  addOutputStatus(context){
    context.commit('addOutputStatus')
  },
  deleteOutputStatus(context, item){
    context.commit('deleteOutputStatus', item)
  },
  addMetadataField(context, payload){
    context.commit('addMetadataField', payload)
  },
  deleteMetadataField(context, item){
    context.commit('deleteMetadataField', item)
  },
  addOutputSpec(context){
    context.commit('addOutputSpec')
  },
  deleteOutputSpec(context, item){
    context.commit('deleteOutputSpec', item)
  },
  resetOutputSpecs(context, item){
    context.commit('resetOutputSpecs', item)
  },
  resetManualMarkers(context, item){
    context.commit('resetManualMarkers', item)
  },
  addManualMarker(context){
    context.commit('addManualMarker')
  },
  deleteManualMarker(context, item){
    context.commit('deleteManualMarker', item)
  },
  addForm(context){
    context.commit('addForm')
  },
  deleteForm(context, item){
    context.commit('deleteForm', item)
  },
}
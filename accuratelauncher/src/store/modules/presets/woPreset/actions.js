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
  addMetadataField(context){
    context.commit('addMetadataField')
  },
  deleteMetadataField(context, item){
    context.commit('deleteMetadataField', item)
  },
}
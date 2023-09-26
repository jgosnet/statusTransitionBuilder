export default {
  updateIgnoreMissingFiles(context, value){
    context.commit('updateIgnoreMissingFiles', value)
  },
  updateEditStartTc(context, value){
    context.commit('updateEditStartTc', value)
  },
  updateStartTc(context, value){
    context.commit('updateStartTc', value)
  },
}
export default {
  addNewAudioItem(context){
    context.commit('addNewAudioItem')
  },
  deleteItem(context, audioItem){
    context.commit('deleteItem', audioItem)
  },
}
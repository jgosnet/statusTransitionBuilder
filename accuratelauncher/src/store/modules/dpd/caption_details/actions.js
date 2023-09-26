export default {
  addNewCaptionItem(context){
    context.commit('addNewCaptionItem')
  },
  deleteItem(context, captionItem){
    context.commit('deleteItem', captionItem)
  },
}
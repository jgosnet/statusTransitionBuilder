export default {
  addNewTbmdItem(context){
    context.commit('addNewTbmdItem')
  },
  deleteItem(context, item){
    context.commit('deleteItem', item)
  },
}
export default {
  addNewItem(context){
    context.commit('addNewItem')
  },
  deleteItem(context, item){
    context.commit('deleteItem', item)
  },
}
export default {
  addNewItem(context){
    context.commit('addNewItem')
  },
  deleteItem(context, item){
    context.commit('deleteItem', item)
  },
  updateUseSpritemap(context, value){
    console.log(`updating to ${value}`)
    context.commit('updateUseSpritemap', value)
  },
}
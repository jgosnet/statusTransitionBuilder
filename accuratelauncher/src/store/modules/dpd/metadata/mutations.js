export default {
  addNewItem(state){
    state.metadata[state.metadataIndex] = {
      keyname: "new",
      jmespath: "",
      index: state.metadataIndex
    };
    state.metadataIndex += 1;
  },
  deleteItem(state, item){
    console.log(`trying to delete: ${item.index}`)
    console.log(item)
    delete state.metadata[item.index];
    for (const index in state.metadata){
      console.log(state.metadata[index])
    }
  },

}
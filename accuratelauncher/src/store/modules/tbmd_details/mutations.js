export default {
  addTbmdItem(state, item){
    state.tbmdItems.push(item)
  },
  addNewTbmdItem(state){
    state.tbmdItems[state.tbmdIndex] = {
      name: "new",
      label: "",
      index: state.tbmdIndex,
      includeAssetName: false,
      assetName: null
    };
    state.tbmdIndex += 1;
  },
  deleteItem(state, item){
    console.log(`trying to delete: ${item.index}`)
    delete state.tbmdItems[item.index];
    console.log(state.tbmdItems)

  },

}
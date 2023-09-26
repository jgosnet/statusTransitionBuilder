export default {
  addDefaultItems(state){
    state.tbmdItems[state.index] = {
      name: "spritemap_image",
      label: "",
      index: state.index,
      includeAssetName: false,
      assetName: null
    };
    state.index += 1;
  },
  deleteItem(state, item){
    console.log(`trying to delete: ${item.index}`)
    delete state.tbmdItems[item.index];
    console.log(state.tbmdItems)

  },
  updateUseSpritemap(state, value){
    console.log(`updating to ${value}`)
    state.useSpritemap = value;
  },

}
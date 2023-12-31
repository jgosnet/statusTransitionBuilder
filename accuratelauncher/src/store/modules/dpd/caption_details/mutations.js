export default {
  addCaptionItem(state, item){
    state.captionItems.push(item)
  },
  addNewCaptionItem(state){
    state.captionItems[state.captionIndex] = {
      name: "new",
      label: "",
      index: state.captionIndex,
      includeAssetName: false,
      assetName: null,
      includeLanguage: false,
      language: null,
      includeFormat: false,
      format: null,
      includeStartTc: false,
      startTc: null,
    };
    state.captionIndex += 1;
  },
  deleteItem(state, captionItem){
    console.log(`trying to delete: ${captionItem.index}`)
    delete state.captionItems[captionItem.index];
    console.log(state.captionItems)
  },

}
export default {
  addAudioItem(state, audioItem){
    state.audioItems.push(audioItem)
  },
  addNewAudioItem(state){
    state.audioItems[state.audioIndex] = {
      name: "new",
      label: "",
      index: state.audioIndex,
      includeAssetName: false,
      includeLanguage: false,
      language: null,
      assetName: null
    };
    state.audioIndex += 1;
  },
  deleteItem(state, audioItem){
    console.log(`trying to delete: ${audioItem.index}`)
    delete state.audioItems[audioItem.index];
    console.log(state.audioItems)

  },

}
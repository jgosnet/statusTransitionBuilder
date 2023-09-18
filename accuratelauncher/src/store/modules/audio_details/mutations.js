export default {
  addAudioItem(state, audioItem){
    state.audioItems.push(audioItem)
  },
  addNewAudioItem(state){
    state.audioItems.push({
      name: "new",
      label: "",
      asset_name: null
    })
  }
}
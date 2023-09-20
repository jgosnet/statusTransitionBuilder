export default {
  updateIgnoreMissingFiles(state, value){
    console.log(`updating value to ${value}`)
    state.ignoreMissingFiles = value;
  },
  updateEditStartTc(state, value){
    state.editStartTc = value;
  },
  updateStartTc(state, value){
    state.startTc = value;
  },
}
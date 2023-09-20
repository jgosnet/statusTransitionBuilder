export default {
  ignoreMissingFiles(state){
    return state.ignoreMissingFiles
  },
  editStartTc(state){
    return state.editStartTc
  },
  startTc(state){
    return state.startTc
  },
  jsonForm(state){
    console.log("getting config from spritemapItems details")
    let res = {
      ignore_missing_labels: state.ignoreMissingFiles,
    }
    if (state.editStartTc){
      res['start_tc'] = state.startTc
    }
    return res
  }
}
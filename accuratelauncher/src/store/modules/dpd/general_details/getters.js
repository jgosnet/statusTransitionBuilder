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
  },
  isValid(state){
    if (state.editStartTc === true &&  !state.startTc){
      return false
    }
    if (state.editStartTc){
      const tcRegexp = "^([0-1][0-9]|[0-2][0-3]):([0-5][0-9]):([0-5][0-9])[:;]([0-6][0-9])$";
      const intRegexp = "^\\d+$";
      if (!state.startTc.match(intRegexp) && !state.startTc.match(tcRegexp)){
        return false
      }
    }

    return true
  }
}
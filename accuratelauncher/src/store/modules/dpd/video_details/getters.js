export default {
  videoLabel(state){
    return state.videoLabel
  },
  videoAssetName(state){
    return state.videoAssetName
  },
  includeAssetName(state){
    return state.includeAssetName
  },
  jsonForm(state){
    console.log("getting config from video details")
    let res = {}
    res['label'] = state.videoLabel
    if (state.includeAssetName){
      res["asset_name"] = state.videoAssetName
    }
    return res
  },
  isValid(state){
    if (!state.videoLabel){
      return false
    }
    if (state.includeAssetName === true &&  !state.videoAssetName){
      return false
    }
    return true
  }
}
export default {
  audioItems(state){
    return state.audioItems
  },
  jsonForm(state){
    console.log("getting config from audio details")
    let res = {}

    for (const index in state.audioItems){
      const item = state.audioItems[index]
      let resData = {
        label: item.label,
      }

      if (item.enabled !== undefined){
        resData['enabled'] = item.enabled
      }

      if (item.includeAssetName === true){
        resData['asset_name'] = item.assetName
      }

      if (item.includeLanguage === true){
        resData['language'] = item.language
      }

      res[item.name] = resData
    }
    return res
  },
  isValid(state){
    for (const index in state.audioItems) {
      const item = state.audioItems[index]
      if (!item.label
        || (item.includeAssetName && !item.assetName)
        || (!item.name)
        || (item.includeLanguage && !item.language)){
        return false
      }
      console.log(item)
    }

    return true
  }
}
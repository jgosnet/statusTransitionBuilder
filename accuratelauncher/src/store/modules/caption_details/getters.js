export default {
  captionItems(state){
    return state.captionItems
  },
  jsonForm(state){
    let res = {}

    for (const index in state.captionItems){
      const item = state.captionItems[index]
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

      if (item.includeStartTc === true){
        resData['start_tc'] = item.startTc
      }

      if (item.includeFormat === true){
        resData['format'] = item.format
      }

      res[item.name] = resData
    }
    return res
  }
}
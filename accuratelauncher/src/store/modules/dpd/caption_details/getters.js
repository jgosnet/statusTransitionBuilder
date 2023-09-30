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
  },
  isValid(state){
    for (const index in state.captionItems){
      const item = state.captionItems[index]
      if (!item.label
        || (item.includeAssetName && !item.assetName)
        || (!item.name)
        || (item.includeLanguage && !item.language)
        || (item.includeFormat && !item.format)
        || (item.includeStartTc && !item.startTc)){
        return false
      }
      if (item.includeStartTc){
        const tcRegexp = "^([0-1][0-9]|[0-2][0-3]):([0-5][0-9]):([0-5][0-9])[:;]([0-6][0-9])$";
        const intRegexp = "^\\d+$";
        if (!item.startTc.match(intRegexp) && !item.startTc.match(tcRegexp)){
          return false
        }
      }
      console.log(item)
    }

    return true
  }
}
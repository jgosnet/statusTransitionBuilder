export default {
  spritemapItems(state){
    return state.spritemapItems
  },
  useSpritemap(state){
    return state.useSpritemap
  },
  jsonForm(state){
    console.log("getting config from spritemapItems details")
    let res = {}

    if (state.useSpritemap === true){
      for (const index in state.spritemapItems){
        const item = state.spritemapItems[index]
        let resData = {
          label: item.label,
        }

        if (item.includeAssetName === true){
          resData['asset_name'] = item.assetName
        }

        res[item.name] = resData
      }
    }

    return res
  },
  isValid(state){
    if (state.useSpritemap === true) {
      for (const index in state.spritemapItems) {
        const item = state.spritemapItems[index]
        if (!item.name
          || (item.includeAssetName && !item.assetName)
          || !item.label){
          return false
        }

        console.log(item)
      }
    }

    return true
  }
}
export default {
  tbmdItems(state){
    return state.tbmdItems
  },
  jsonForm(state){
    console.log("getting config from tbmd details")
    let res = {}

    for (const index in state.tbmdItems){
      const item = state.tbmdItems[index]
      let resData = {
        label: item.label,
      }

      if (item.includeAssetName === true){
        resData['asset_name'] = item.assetName
      }

      res[item.name] = resData
    }
    return res
  }
}
export default {
  metadata(state){
    return state.metadata
  },
  // eslint-disable-next-line no-unused-vars
  jsonForm(state, getters, rootState, rootGetters){
    console.log("getting config from metadata")
    console.log(state.metadata)
    let res = []
    const metadataList = rootGetters['woPreset/metadataFields']
    for (const index in metadataList){
      const item = metadataList[index]
      if (item.source === 'metadata' && item.autoPopulate === true){
        res.push({
          key: item.key,
          jmespath: item.jmespath,
        })
      }
    }
    return res
  }
}
export default {
  metadata(state){
    return state.metadata
  },
  // eslint-disable-next-line no-unused-vars
  jsonForm(state){
    console.log("getting config from metadata")
    console.log(state.metadata)
    let res = []
    for (const index in state.metadata){
      const item = state.metadata[index]
      res.push({
        key: item.keyname,
        jmespath: item.jmespath,
      })
    }
    return res
  }
}
export default {
  spritemapItems(state){
    return state.spritemapItems
  },
  useSpritemap(state){
    return state.useSpritemap
  },
  jsonForm(state){
    console.log("getting config from spritemapItems details")
    return state.spritemapItems
  }
}
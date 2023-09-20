export default {
  // eslint-disable-next-line no-unused-vars
  jsonForm(state, getters, rootState, rootGetters){
    console.log("test123")
    console.log(rootState)
    // eslint-disable-next-line no-unused-vars
    const videoDetails = rootGetters["videoDetails/jsonForm"];
    const audioDetails = rootGetters["audioDetails/jsonForm"];
    const captionDetails = rootGetters["captionDetails/jsonForm"];
    const tbmdDetails = rootGetters["tbmdDetails/jsonForm"];

    let res = {}
    res['ignore_missing_labels'] = rootGetters['generalDetails/ignoreMissingFiles']
    if (rootGetters['generalDetails/editStartTc']){
      res['start_tc'] = rootGetters['generalDetails/startTc']
    }
    res['video_details'] = videoDetails
    res['audio_details'] = audioDetails
    res['caption_details'] = captionDetails
    res['tbmd_details'] = tbmdDetails
    return res
  },
  // eslint-disable-next-line no-unused-vars
  isValid(state, getters, rootState, rootGetters){
    return false
  },
}
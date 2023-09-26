import videoDetailsState from "@/store/modules/dpd/video_details/state";
import videoDetailsActions from "@/store/modules/dpd/video_details/actions";
import videoDetailsGetters from "@/store/modules/dpd/video_details/getters";
import videoDetailsMutations from "@/store/modules/dpd/video_details/mutations";

export default {
  namespaced: true,
  state: videoDetailsState,
  getters: videoDetailsGetters,
  mutations: videoDetailsMutations,
  actions: videoDetailsActions
}

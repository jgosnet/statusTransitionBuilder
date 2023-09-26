import captionDetailsState from "@/store/modules/dpd/caption_details/state";
import captionDetailsActions from "@/store/modules/dpd/caption_details/actions";
import captionDetailsGetters from "@/store/modules/dpd/caption_details/getters";
import captionDetailsMutations from "@/store/modules/dpd/caption_details/mutations";

export default {
  namespaced: true,
  state: captionDetailsState,
  getters: captionDetailsGetters,
  mutations: captionDetailsMutations,
  actions: captionDetailsActions
}

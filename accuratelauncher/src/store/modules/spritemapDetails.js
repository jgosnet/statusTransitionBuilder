import spritemapDetailsState from "@/store/modules/spritemap_details/state";
import spritemapDetailsActions from "@/store/modules/spritemap_details/actions";
import spritemapDetailsGetters from "@/store/modules/spritemap_details/getters";
import spritemapDetailsMutations from "@/store/modules/spritemap_details/mutations";

export default {
  namespaced: true,
  state: spritemapDetailsState,
  getters: spritemapDetailsGetters,
  mutations: spritemapDetailsMutations,
  actions: spritemapDetailsActions
}

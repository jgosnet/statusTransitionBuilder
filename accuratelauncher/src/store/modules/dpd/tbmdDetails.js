import tbmdDetailsState from "@/store/modules/dpd/tbmd_details/state";
import tbmdDetailsActions from "@/store/modules/dpd/tbmd_details/actions";
import tbmdDetailsGetters from "@/store/modules/dpd/tbmd_details/getters";
import tbmdDetailsMutations from "@/store/modules/dpd/tbmd_details/mutations";

export default {
  namespaced: true,
  state: tbmdDetailsState,
  getters: tbmdDetailsGetters,
  mutations: tbmdDetailsMutations,
  actions: tbmdDetailsActions
}

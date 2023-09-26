import generalDetailsState from "@/store/modules/dpd/general_details/state";
import generalDetailsActions from "@/store/modules/dpd/general_details/actions";
import generalDetailsGetters from "@/store/modules/dpd/general_details/getters";
import generalDetailsMutations from "@/store/modules/dpd/general_details/mutations";

export default {
  namespaced: true,
  state: generalDetailsState,
  getters: generalDetailsGetters,
  mutations: generalDetailsMutations,
  actions: generalDetailsActions
}

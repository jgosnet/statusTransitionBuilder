import generalDetailsState from "@/store/modules/general_details/state";
import generalDetailsActions from "@/store/modules/general_details/actions";
import generalDetailsGetters from "@/store/modules/general_details/getters";
import generalDetailsMutations from "@/store/modules/general_details/mutations";

export default {
  namespaced: true,
  state: generalDetailsState,
  getters: generalDetailsGetters,
  mutations: generalDetailsMutations,
  actions: generalDetailsActions
}

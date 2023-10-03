import prerequisitesState from "@/store/modules/prerequisites/state";
import prerequisitesActions from "@/store/modules/prerequisites/actions";
import prerequisitesGetters from "@/store/modules/prerequisites/getters";
import prerequisitesMutations from "@/store/modules/prerequisites/mutations";

export default {
  namespaced: true,
  state: prerequisitesState,
  getters: prerequisitesGetters,
  mutations: prerequisitesMutations,
  actions: prerequisitesActions
}

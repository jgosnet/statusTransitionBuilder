import statusState from "@/store/modules/status/state";
import statusActions from "@/store/modules/status/actions";
import statusGetters from "@/store/modules/status/getters";
import statusMutations from "@/store/modules/status/mutations";

export default {
  namespaced: true,
  state: statusState,
  getters: statusGetters,
  mutations: statusMutations,
  actions: statusActions
}

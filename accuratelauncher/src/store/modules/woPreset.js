import woPresetState from "@/store/modules/woPreset/state";
import woPresetActions from "@/store/modules/woPreset/actions";
import woPresetGetters from "@/store/modules/woPreset/getters";
import woPresetMutations from "@/store/modules/woPreset/mutations";

export default {
  namespaced: true,
  state: woPresetState,
  getters: woPresetGetters,
  mutations: woPresetMutations,
  actions: woPresetActions
}

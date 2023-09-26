import woPresetState from "@/store/modules/presets/woPreset/state";
import woPresetActions from "@/store/modules/presets/woPreset/actions";
import woPresetGetters from "@/store/modules/presets/woPreset/getters";
import woPresetMutations from "@/store/modules/presets/woPreset/mutations";

export default {
  namespaced: true,
  state: woPresetState,
  getters: woPresetGetters,
  mutations: woPresetMutations,
  actions: woPresetActions
}

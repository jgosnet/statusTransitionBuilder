import launcherPresetState from "@/store/modules/presets/launcherPreset/state";
import launcherPresetActions from "@/store/modules/presets/launcherPreset/actions";
import launcherPresetGetters from "@/store/modules/presets/launcherPreset/getters";
import launcherPresetMutations from "@/store/modules/presets/launcherPreset/mutations";

export default {
  namespaced: true,
  state: launcherPresetState,
  getters: launcherPresetGetters,
  mutations: launcherPresetMutations,
  actions: launcherPresetActions
}

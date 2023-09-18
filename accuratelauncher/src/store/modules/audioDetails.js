import audioDetailsState from "@/store/modules/audio_details/state";
import audioDetailsActions from "@/store/modules/audio_details/actions";
import audioDetailsGetters from "@/store/modules/audio_details/getters";
import audioDetailsMutations from "@/store/modules/audio_details/mutations";

export default {
  namespaced: true,
  state: audioDetailsState,
  getters: audioDetailsGetters,
  mutations: audioDetailsMutations,
  actions: audioDetailsActions
}

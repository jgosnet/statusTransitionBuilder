import metadataDetailsState from "@/store/modules/metadata/state";
import metadataDetailsActions from "@/store/modules/metadata/actions";
import metadataDetailsGetters from "@/store/modules/metadata/getters";
import metadataDetailsMutations from "@/store/modules/metadata/mutations";

export default {
  namespaced: true,
  state: metadataDetailsState,
  getters: metadataDetailsGetters,
  mutations: metadataDetailsMutations,
  actions: metadataDetailsActions
}

import metadataDetailsState from "@/store/modules/dpd/metadata/state";
import metadataDetailsActions from "@/store/modules/dpd/metadata/actions";
import metadataDetailsGetters from "@/store/modules/dpd/metadata/getters";
import metadataDetailsMutations from "@/store/modules/dpd/metadata/mutations";

export default {
  namespaced: true,
  state: metadataDetailsState,
  getters: metadataDetailsGetters,
  mutations: metadataDetailsMutations,
  actions: metadataDetailsActions
}

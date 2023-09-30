import {createStore} from 'vuex'

import configuration from "@/store/modules/configuration";
import videoDetails from "@/store/modules/dpd/videoDetails";
import audioDetails from "@/store/modules/dpd/audioDetails";
import captionDetails from "@/store/modules/dpd/captionDetails";
import tbmdDetails from "@/store/modules/dpd/tbmdDetails";
import spritemapDetails from "@/store/modules/dpd/spritemapDetails";
import generalDetails from "@/store/modules/dpd/generalDetails";
import metadata from "@/store/modules/dpd/metadata";
import snackbar from "@/store/modules/snackbar";
import woPreset from "@/store/modules/woPreset";
import launcherPreset from "@/store/modules/launcherPreset";


export const store = createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    snackbar,
    configuration,
    videoDetails,
    audioDetails,
    captionDetails,
    tbmdDetails,
    spritemapDetails,
    generalDetails,
    metadata,
    woPreset,
    launcherPreset,
  }
})

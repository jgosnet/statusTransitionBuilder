import {createStore} from 'vuex'

import configuration from "@/store/modules/configuration";
import videoDetails from "@/store/modules/videoDetails";
import audioDetails from "@/store/modules/audioDetails";
import captionDetails from "@/store/modules/captionDetails";
import tbmdDetails from "@/store/modules/tbmdDetails";
import spritemapDetails from "@/store/modules/spritemapDetails";
import generalDetails from "@/store/modules/generalDetails";
import snackbar from "@/store/modules/snackbar";

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
  }
})

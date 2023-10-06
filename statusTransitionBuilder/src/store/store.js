import {createStore} from 'vuex'

import status from "@/store/modules/status";
import snackbar from "@/store/modules/snackbar";


export const store = createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    snackbar,
    status,
  }
})

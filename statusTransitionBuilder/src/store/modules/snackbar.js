/*
    Allows to use 1 central snackbar component across the app

*/
const state = {
  message: '',
  messageList: [],
  timeout: 0,
  color: 'red',
  snackbarDialog: true,
}

const getters = {
  snackbarDialog(state){
    return state.snackbarDialog
  }
}

const mutations = {
  showMessage: (state, payload) => {
    state.snackbarDialog = false;
    state.timeout = 5000;

    if (payload.message !== undefined){
      state.message = payload.message;
    }

    if (payload.messageList !== undefined){
      state.messageList = payload.messageList;
    }
    state.color = payload.color;
    state.snackbarDialog = true;
  },

  closeMessage: (state) => {
    state.snackbarDialog = false;
    state.timeout = 0;
    state.message = '';
    state.messageList = [];
    state.color = '';
  },

  setSnackbarDialog(state, value){
    state.snackbarDialog = value;
  },
}


const actions = {
  showMessage({ commit }, payload){
    commit('closeMessage', payload)
    commit('showMessage', payload)
  },

  closeMessage({ commit }, payload){
    commit('closeMessage', payload)
  },

  setSnackbarDialog({ commit }, payload){
    commit('setSnackbarDialog', payload)
  },
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}

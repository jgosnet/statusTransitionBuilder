<template lang="pug">
v-snackbar(
    v-model='snackbarDialog'
    :timeout='timeout'
    :color='color'
    multi-line
  )
  | {{message}}
  ul
    li(v-for='item in messageList' :key='item')
      | {{item}}
  template(#actions)
    v-btn(
      color="blue"
      variant="text"
      @click="snackbarDialog = false"
    ) Close
    //v-col(cols="2")
    //  v-btn(:color='closeButtonColor' @click='closeMessage')
    //    v-icon(icon="fas fa-times")
</template>

<script>
import {mapState, mapActions} from 'vuex';

export default {
  name: "SnackBarPopup",
  computed: {
    ...mapState('snackbar', [
      'timeout',
      'message',
      'color',
      'messageList'
    ]),

    snackbarDialog: {
      set(value){
        this.$store.dispatch('snackbar/setSnackbarDialog', value);
      },
      get() {
        return this.$store.getters['snackbar/snackbarDialog'];
      }
    },

    closeButtonColor(){
      return this.color === 'red' ? 'white' : 'red';
    }
  },
  methods:{
    ...mapActions('snackbar', ['closeMessage', 'setSnackbarDialog'])
  }
}
</script>

<style scoped>

</style>
<template lang="pug">
v-card.rounded-lg.mx-0
  v-card-text.float-left
    v-row
      v-btn.mx-2.my-1(
        prepend-icon="fa-solid fa-copy"
        v-clipboard="jsonForm"
        v-clipboard:success="clipboardSuccessHandler"
        v-clipboard:error="clipboardErrorHandler"
        ) Copy
      v-alert.float-right(title="Copied to clipboard."
        type="success"
        color="success"
        density="compact"
        v-show="dismissCountDown > 0")

    v-row.left-align.pt-2
      v-icon(:icon="validationIcon" :color="validationStatus")
      span.pl-1 {{ validationMessage }}

    v-row.left-align
      json-viewer(:value="jsonForm"
      expanded=true
      :expand-depth="expandDepth"
      theme="my-awesome-json-theme")
    //v-btn(@click="refresh") refresh


</template>

<script>


import {mapGetters} from "vuex";

export default {
  name: "JsonViewerPage",
  data: function() {
    return {
      expandDepth: 5,
      dismissSecs: 5,
      dismissCountDown: 0,
      stringOutput: "test123",
    }
  },
  computed: {
    ...mapGetters(["jsonForm", "isValid"]),
    validationStatus(){
      // try to validate all parts
      if (this.isValid){
        return "green"
      } else {
        return "red"
      }

    },
    validationIcon(){
      if (this.isValid){
        return "fa-regular fa-circle-check"
      } else {
        return "fa-solid fa-circle-xmark"
      }
    },
    validationMessage() {
      if (this.isValid) {
        return "Form is complete"
      } else {
        return "Invalid"
      }
    },
  },
  methods: {
    refresh(){
      console.log(this.$store.getters["jsonForm"])
    },
    // eslint-disable-next-line no-unused-vars
    clipboardSuccessHandler () {
      console.log('success')
      this.dismissCountDown = this.dismissSecs
      setTimeout(() => {
        this.dismissCountDown = 0
      }, 3000)
    },

    // eslint-disable-next-line no-unused-vars
    clipboardErrorHandler () {
      console.log('error')
    }
  }
}
</script>

<style scoped>


</style>
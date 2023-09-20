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
      expanded="true"
      expand-depth="5"
      theme="my-awesome-json-theme")
    //v-btn(@click="refresh") refresh


</template>

<script>


import {mapGetters} from "vuex";

export default {
  name: "JsonViewerPage",
  data: function() {
    return {
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

.jv-number { color: #fc1e70 }

.my-awesome-json-theme {
  background: #fff;
  white-space: nowrap;
  color: #525252;
  font-size: 14px;
  font-family: Consolas, Menlo, Courier, monospace;

  .jv-ellipsis {
    color: #999;
    background-color: #eee;
    display: inline-block;
    line-height: 0.9;
    font-size: 0.9em;
    padding: 0px 4px 2px 4px;
    border-radius: 3px;
    vertical-align: 2px;
    cursor: pointer;
    user-select: none;
  }

   .jv-button { color: #49b3ff }
  .jv-key { color: #111111 }
  .jv-item {
    &.jv-array { color: #111111 }
    &.jv-boolean { color: #fc1e70 }
    &.jv-function { color: #067bca }
    &
    &.jv-number-float { color: #fc1e70 }
    &.jv-number-integer { color: #fc1e70 }
    &.jv-object { color: #111111 }
    &.jv-undefined { color: #e08331 }
    &.jv-string {
      color: #42b983;
      word-break: break-word;
      white-space: normal;
    }
  }
  .jv-code {
    .jv-toggle {
      &:before {
        padding: 0px 2px;
        border-radius: 2px;
      }
      &:hover {
        &:before {
          background: #eee;
        }
      }
    }
  }
}

</style>
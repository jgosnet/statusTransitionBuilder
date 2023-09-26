<template lang="pug">
v-window-item(value="rallyConfig" )
  v-row.my-1
    v-btn.mx-2.my-1(
      prepend-icon="fa-solid fa-copy"
      v-clipboard="woRallyConfig"
      v-clipboard:success="clipboardSuccessHandler"
      v-clipboard:error="clipboardErrorHandler"
      ) Copy
    v-alert.float-right(title="Copied to clipboard."
      type="success"
      color="success"
      density="compact"
      v-show="dismissCountDown > 0")

  v-row.mx-1
    | {{woRallyConfig}}
</template>

<script>
export default {
  name: "RallyConfig",
  data(){
    return {
      dismissSecs: 5,
      dismissCountDown: 0,
    }
  },
  methods:{
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
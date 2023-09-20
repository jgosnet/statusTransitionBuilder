<template lang="pug">
v-dialog(v-model="isVisible"
  ref="popup"
  width="auto")
  v-card
    v-card-text
      slot(name="message")
        | {{this.message}}
    v-card-actions
      slot(name="actions")
        v-spacer
        v-btn(color="primary" @click="_cancel()") Cancel
        v-btn(color="primary"  @click="_confirm()") Confirm


</template>

<script>
export default {
  name: "ConfirmDialog",
  props:{
  },
  data(){
    return {
      isVisible: false,
      title: undefined,
      message: undefined, // Main text content
      okButton: undefined, // Text for confirm button; leave it empty because we don't know what we're using it for
      cancelButton: 'Go Back', // text for cancel button

      // Private variables
      resolvePromise: undefined,
      rejectPromise: undefined,
    }
  },
  methods: {
    openDialog(){
      this.isVisible = true
    },
    closeDialog(){
      this.isVisible = false
    },
    show(opts = {}) {
      console.log("trying to show")
      this.message = opts.message
      this.okButton = opts.okButton

      // Once we set our config, we tell the popup modal to open
      this.isVisible = true
      // Return promise so the caller can get results
      return new Promise((resolve, reject) => {
          this.resolvePromise = resolve
          this.rejectPromise = reject
      })
    },

    _confirm() {
        this.isVisible = false
        this.resolvePromise(true)
    },

    _cancel() {
        this.isVisible = false
        this.resolvePromise(false)
        // Or you can throw an error
        // this.rejectPromise(new Error('User canceled the dialogue'))
    },
  }
}
</script>

<style scoped>

</style>
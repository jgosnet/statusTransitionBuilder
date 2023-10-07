<template lang="pug">
v-dialog(v-model="stepNameForm").w-50
  template(v-slot:default="{ isActive }")
    v-card
      v-card-title test Form
      v-card-text
        v-row.px-3.py-1
          v-col(cols="12").py-1.my-0
            | test123
      v-card-actions
        v-spacer
        v-btn(@click="closeForm()") Cancel
        //v-btn(@click="confirm()" :disabled="!newFormIsValid" ) confirm
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "testForm",
  computed: {
    ...mapGetters('status', ['stepNameForm'])
  },
  methods:{
    closeForm(){
      this.$store.dispatch('status/updateStepForm', false);
    }
  }
}
</script>

<style scoped>

</style>
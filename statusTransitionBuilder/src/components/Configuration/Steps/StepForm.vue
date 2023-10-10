<template lang="pug">
div
  v-dialog(v-model="isActive").w-50
    template(v-slot:activator="{ props }")
      v-btn(v-show="!this.item"
        size="small" v-bind="props")
        v-icon fa-solid fa-plus

      v-icon(color="blue" v-show="this.item"
        size="small"  v-bind="props") fa-solid fa-pen-to-square
    template(v-slot:default="{ isActive }")
      v-card
        v-card-title New Step Name
        v-card-text
          v-row.px-3.py-1
            v-col(cols="12").py-1.my-0
              v-text-field(  v-model="stepName" hide-details @keyup.enter="confirm()"
                label="Step Name" density="compact" autofocus)
        v-card-actions
          v-spacer
          v-btn(@click="this.isActive = false") Cancel
          v-btn(@click="confirm()" :disabled="!newFormIsValid" ) confirm
</template>

<script>
export default {
  name: "StepForm",
  props: ['item'],
  data(){
    return {
      stepName: this.item ? this.item.name : "",
      isActive: false,
    }
  },
  computed: {
    newFormIsValid(){
      if (this.stepName){
        return true
      }
      return false
    },
  },
  methods: {
    confirm(){
      this.isActive = false;

      let payload = {
        name: this.stepName
      };
      console.log(this.item);
      if (this.item && this.item.index !== undefined){
        console.log('Updating existing Stepname');
        payload['index'] = this.item.index;
        this.$store.dispatch('status/updateStep', payload);
      } else {
        console.log('Adding new Stepname');
        this.$store.dispatch('status/addStep', payload);
        this.resetForm();
      }

    },
    resetForm(){
      this.stepName = ""
    }
  },
  mounted() {

  }
}
</script>

<style scoped>

</style>
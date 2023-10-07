<template lang="pug">
div
  v-row.px-3.py-1
    v-col(cols="12").py-1.my-0
      v-text-field(prepend-icon="fa-solid fa-magnifying-glass"
        v-model="search" hide-details
          label="Filter"
          density="compact" )
  v-row.px-3.py-1
    v-col(cols="1").py-1.my-0
      //v-icon(@click="openNewForm") fa-solid fa-user
      //test-form
      StepForm()

    v-col(cols="11").py-1.my-0
      span(v-if="!this.status.length" ) No Steps.
      div(v-else)
        div(v-show="step.name.includes(search)"
          v-for="step in this.status"
          :key="step.index"
          )
          StepItem(:item="step").mb-3


</template>

<script>
import {mapGetters} from "vuex";
import draggable from "vuedraggable";
import StepItem from "@/components/Configuration/StepItem";
import StepForm from "@/components/Configuration/Steps/StepForm";
import TestForm from "@/components/Configuration/Steps/testForm";

export default {
  name: "StepsView",
  components:{
    TestForm,
    StepForm,
    StepItem,
    draggable,
  },
  data(){
    return {
      tab: "asset",
      isExpanded: true,
      search: "",
    }
  },
  computed: {
    ...mapGetters('status', ['status']),
  },
  methods: {
    openNewForm(){
      this.$store.dispatch('status/updateStepForm', true);
    }
  }
}
</script>

<style scoped>

</style>
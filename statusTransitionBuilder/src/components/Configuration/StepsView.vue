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
      v-btn(size="small" @click="addStep")
        v-icon fa-solid fa-plus
    v-col(cols="11").py-1.my-0
      //| statuses: --{{this.status}}--
      span(v-show="!this.status.length" ) No Steps.
      div(v-for="step in this.status" :key="step.index" v-show="step.name.includes(search)" )
        StepItem(:item="step").mb-3


</template>

<script>
import {mapGetters} from "vuex";
import draggable from "vuedraggable";
import StepItem from "@/components/Configuration/StepItem";


export default {
  name: "StepsView",
  components:{
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
    statusList(){
      let res = [];
      // for (const statusItem of this.$store.getters['status/status']){
      //   console.log(statusItem)
      //   res.push(statusItem)
      // }
      return res
    }
  },
  methods: {
    addStep(){
      this.$store.dispatch("status/addStep")
    }
  }
}
</script>

<style scoped>

</style>
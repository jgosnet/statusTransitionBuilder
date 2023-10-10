<template lang="pug">
v-card.mb-2.py-0(elevation="6" )
  v-card-text.ma-0.pa-1
    v-row.px-3.pt-1
      v-col(cols="1")
        v-icon.handle1.float-left fa-solid fa-bars
      v-col(cols="4")
        v-select(v-model="item.opType" hide-details
                      label="Type" density="compact" :items="possibleOperations")
      v-col(cols="6")
        v-select(v-if="item.opType !== 'clear'"
          v-model="item.keys" hide-details :items="possibleKeys" multiple
                label="Keys" density="compact")
        v-select(v-else
          v-model="item.groups" hide-details :items="possibleGroups" multiple
              label="Groups" density="compact")
      v-col(cols="1")
        v-icon.handle.float-right(color="red" @click="deleteOperation()" size="x-large" ) fa-solid fa-xmark

    v-row.px-3.py-1
      v-col(:cols="localOtherStepName ? 1 : 12").py-1
        v-checkbox(v-model="localOtherStepName" hide-details
          :label="localOtherStepName ? '': 'select step name ?'" density="compact" )
      v-col(v-show="localOtherStepName" cols="6").py-1.pb-3
         v-select(v-model="localStepName" hide-details
          label="Step name" density="compact" :items="this.statusListMinusCurrent")

</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "StepItemTransitionsOperationItem",
  props: ['item', 'parent'],
  data(){
    return {
      localOtherStepName: this.item.otherStepName || false,
      localStepName: this.item.stepName || '',
    }
  },
  computed: {
    ...mapGetters('status', ['possibleOperations', 'statusList', 'possibleGroups']),
    statusListMinusCurrent(){
      return this.$store.getters['status/status'].filter(obj => obj.index !== this.parent.index).map(obj => obj.name);
      // return this.$store.getters['status/status']
    },
    possibleKeys(){
      if (!this.item.otherStepName){
        return this.parent.status.map(obj => obj.name)
      }

      const stepnames = this.$store.getters['status/status'];
      console.log(this.item.stepName);
      console.log(stepnames.filter(obj => obj.name === this.item.stepName))
      const foundStepname = stepnames.filter(obj => obj.name === this.item.stepName)
      if (foundStepname === undefined || foundStepname.length === 0){
        return []
      } else {
        let res = [];
        for (const statusItem of foundStepname[0].status){
          res.push(statusItem.name);
        }
        return res;
      }
    }
  },
  methods: {
    deleteOperation(element){
      // eslint-disable-next-line vue/no-mutating-props
      this.item.operations = this.item.operations.filter(obj => obj.index !== element.index);
    },
  },
  watch: {
    localOtherStepName(newValue, oldValue){
      if (newValue !== oldValue){
        console.log('value of otherstepname changed')
        // eslint-disable-next-line vue/no-mutating-props
        this.item.keys = [];
      }
      // eslint-disable-next-line vue/no-mutating-props
      this.item.otherStepName = newValue;
    },
    localStepName(newValue, oldValue){
      if (newValue !== oldValue){
        console.log('value of localStepName changed')
        // eslint-disable-next-line vue/no-mutating-props
        this.item.keys = [];
      }
      // eslint-disable-next-line vue/no-mutating-props
      this.item.stepName = newValue;
    }
  }
}
</script>

<style scoped>

</style>
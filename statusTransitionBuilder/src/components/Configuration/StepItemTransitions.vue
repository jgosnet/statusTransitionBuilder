<template lang="pug">
v-card
  v-card-title(@click="isExpanded = !isExpanded").left-align.pl-2
    b.px-4 Transitions
    | ({{item.transitions.length}} items)
    //v-icon.ml-3(size="x-small" ) fa-solid fa-trash-can
    v-icon.float-right.bg-transparent(:icon="expansionIcon" size="x-large"
      )
  div(v-show="!isExpanded").py-1

  div(v-show="isExpanded").mb-3
    v-row.px-3.py-1
      v-col(cols="1").py-1.my-0
        v-btn(size="small" @click="addTransition")
          v-icon fa-solid fa-plus
      v-col(cols="11").py-1.my-0
        span(v-show="!item.transitions.length" ) No Transitions.
        draggable(v-model="item.transitions"
                handle=".handle"
                :group="item.index"
                @start="drag=true"
                @end="drag=false"
                item-key="index").w-100

          template(#item="{element}")
            v-card.mb-2.py-0(elevation="6" )
              v-card-text.ma-0.pa-1
                v-row.px-3.pt-1
                  v-col(cols="1")
                    v-icon.handle.float-left fa-solid fa-bars
                  v-col(cols="10")
                    div.float-left
                      v-icon( @click="element.isExpanded = !element.isExpanded" size="large"
                          :icon="!element.isExpanded ? 'fa-solid fa-pen-to-square' : 'fa-solid fa-check'"
                          :color="!element.isExpanded ? 'blue' :'green'"
                          ).pb-2.pr-5.mr-5
                      b(v-show="!element.isExpanded" ).pr-5 {{element.name}}
                    v-text-field(v-show="element.isExpanded" v-model="element.name" hide-details
                            label="Name" density="compact" variant="outlined" )

                  v-col(cols="1")
                    v-icon.handle.float-right(color="red" @click="deleteElement(element)" size="x-large" ) fa-solid fa-xmark

                div(v-show="element.isExpanded" )
                  StepItemTransitionsOperation(:item="element").mb-2

</template>

<script>
import draggable from "vuedraggable";
import {mapGetters} from "vuex";
import StepItemTransitionsOperation from "@/components/Configuration/StepItemTransitionsOperation";

export default {
  name: "StepItemTransitions",
  components: {
    StepItemTransitionsOperation,
    draggable,
  },
  props: ['item'],
  data(){
    return {
      isExpanded: true,
      transitionIndex: 0,
    }
  },
  computed: {
    ...mapGetters('status', []),
    expansionIcon() {
      if (this.isExpanded === false) {
        return "fa-solid fa-caret-down"
      } else {
        return "fa-solid fa-caret-right"
      }
    },
  },
  methods: {
    addTransition(){
      // eslint-disable-next-line vue/no-mutating-props
      this.item.transitions.push({
        index: this.transitionIndex,
        name: '',
        operations: [],
        operationIndex: 0,
        isExpanded: true,
      })
      this.transitionIndex += 1;
    },
    deleteElement(element){
      // eslint-disable-next-line vue/no-mutating-props
      this.item.transitions = this.item.transitions.filter(obj => obj.index !== element.index);
    }
  }
}
</script>

<style scoped>

</style>
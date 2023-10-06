<template lang="pug">
v-card
  v-card-title(@click="isExpanded = !isExpanded").left-align.pl-2
    b.px-4 Status list
    | ({{item.status.length}} items)
    //v-icon.ml-3(size="x-small" ) fa-solid fa-trash-can
    v-icon.float-right.bg-transparent(:icon="expansionIcon" size="x-large"
      )
  div(v-show="!isExpanded").py-1

  div(v-show="isExpanded").mb-3
    v-row.px-3.py-1
      v-col(cols="1").py-1.my-0
        v-btn(size="small" @click="addStatus")
          v-icon fa-solid fa-plus
      v-col(cols="11").py-1.my-0
        span(v-show="!item.status.length" ) No Status.
        draggable(v-model="item.status"
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
                      b.pr-5 {{element.name}}
                      v-icon(:color="element.color" :icon="element.icon" size="x-large" )
                      span.pl-2.pr-2 {{element.group}}: {{element.message }}

                  v-col(cols="1")
                    v-icon.handle.float-right(color="red" @click="deleteElement(element)" size="x-large" ) fa-solid fa-xmark

                div(v-show="element.isExpanded" )
                  v-row.px-3.py-1
                    v-col(cols="3")
                      v-text-field(v-model="element.name" hide-details
                            label="Name" density="compact" variant="outlined" )
                    v-col(cols="4")
                      v-combobox(v-model="element.group" hide-details
                            label="Group" density="compact" :items="possibleGroups" )
                    v-col(cols="5")
                      v-combobox(v-model="element.message" hide-details
                            label="Message" density="compact" :items="possibleMessages")

                  v-row.px-3.py-1
                    v-col(cols="5")
                      v-text-field(v-model="element.icon" hide-details
                            label="Icon" density="compact")
                    v-col(cols="1").pt-5.mr-2
                      color-picker.ml-5(v-model:pureColor="element.color" format="hex6")
                    v-col(cols="3")
                      v-text-field(v-model="element.color" hide-details
                            label="Color" density="compact")

                  v-row.px-3.py-1
                    v-col(:cols="element.includeNotification ? 1 : 12").py-1
                      v-checkbox(v-model="element.includeNotification" hide-details
                        :label="element.includeNotification ? '': 'Include notification ?'" density="compact" )
                    v-col(v-show="element.includeNotification" cols="6").py-1
                      v-text-field(v-model="element.subject" hide-details
                        label="Notification Subject" density="compact")
                    v-col(v-show="element.includeNotification" cols="5").py-1
                      v-combobox(v-model="element.endpoints" hide-details clearable=""
                            label="Endpoints" density="compact" :items="possibleEndpoints" multiple="" chips)

                  v-row.px-3.py-1(v-show="element.includeNotification")
                    StepItemStatusMetadata(:item="element")

                  v-row.px-3.py-1(v-show="element.includeNotification")
                    v-col(cols="12").pb-2.pt-0
                      v-combobox(v-model="element.attachments" hide-details clearable
                            label="Attachments (labels)" density="compact" multiple chips)
              //  "include_metadata": [
              //      ("details", "asset_details"),
              //      ("id", "asset_details.id")
              //  ],
              //  "attachments": ["{label}_pdf_report"]

</template>

<script>
import draggable from "vuedraggable";
import {mapGetters} from "vuex";
import StepItemStatusMetadata from "@/components/Configuration/StepItemStatusMetadata";

export default {
  name: "StepItemStatus",
  components: {
    StepItemStatusMetadata,
    draggable,
  },
  props: ['item'],
  data(){
    return {
      isExpanded: true,
      statusIndex: 0,
    }
  },
  computed: {
    ...mapGetters('status', ['possibleGroups', 'possibleMessages', 'possibleEndpoints']),
    expansionIcon() {
      if (this.isExpanded === false) {
        return "fa-solid fa-caret-down"
      } else {
        return "fa-solid fa-caret-right"
      }
    },
  },
  methods: {
    addStatus(){
      // eslint-disable-next-line vue/no-mutating-props
      this.item.status.push({
        index: this.statusIndex,
        name: '',
        message: '',
        group: '',
        icon: 'fa-solid fa-file',
        color: 'blue',
        includeNotification: false,
        subject: '',
        endpoints: [],
        includeMetadata: [],
        metadataIndex: 0,
        attachments: [],
        isExpanded: true,
      })
      this.statusIndex += 1;
    },
    deleteElement(element){
      // eslint-disable-next-line vue/no-mutating-props
      this.item.status = this.item.status.filter(obj => obj.index !== element.index);
    }
  }
}
</script>

<style scoped>

</style>
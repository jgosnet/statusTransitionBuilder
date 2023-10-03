<template lang="pug">
v-container(fluid).no-border
  v-row(justify="space-around")
    v-timeline(align="start")
      v-timeline-item(icon="fa-solid fa-list-check" dot-color="#B0C8D8" size="x-large"  fill-dot
        @click="$router.push('/prerequisites')").pointer
        v-card(elevation="3" )
          v-card-title
            | [Presets]
            b  Prerequisites
          v-card-text
            p The Accurate launcher relies on a few modules developped by SDVI's Solutions Architecture team. These modules need to be deployed as importable files in Rally.



      v-timeline-item(icon="fa-solid fa-indent" dot-color="grey" size="x-large"  fill-dot
        @click="$router.push('/dpd')").pointer
        v-card(elevation="3" )
          v-card-title
            | [input]
            b  Dynamic preset data
          v-card-text
            p The accurate Launcher module expects a simplified JSON version of the Accurate WO. All the technical specs are determined based on the label/asset provided


      v-timeline-item(icon="fa-solid fa-bolt" dot-color="yellow" size="x-large" fill-dot
      @click="$router.push('/launcher')").pointer
        v-card.w-100(elevation="3" )
          v-card-title
            | [Decision Engine]
            b  Accurate Launcher
          v-card-text
            p The accurate launcher is the first step in the supply chain, and relies on a module created by the SDVI SA team to facilitate the creation of an Accurate WO: Basic, validate, edit.

      v-timeline-item(icon="fa-solid fa-user-check" dot-color="blue" size="x-large" fill-dot
      @click="$router.push('/preset')").pointer
        v-card.w-100(elevation="3" )
          v-card-title
            | [Gateway WO]
            b  Accurate WO
          v-card-text
            p Describes the Accurate WO: ProviderData & RallyConfig required to run with the data passed from the accurate launcher.

      v-timeline-item(icon="fa-solid fa-clipboard-check" dot-color="green" size="x-large" fill-dot)
        v-card.w-100(elevation="3" )
          v-card-title
            | [Decision Engine]
            |
            b Check result
          v-card-text
            p Not available yet

    v-spacer
    v-img.pt-5.w-100.faded(:src="accurateImage" )

</template>

<script>

export default {
  name: "TheHome",
  data(){
    return {
      accurateImage: require('@/assets/images/accurate.png')
    }
  }
}
</script>

<style scoped>
.pointer{
 cursor: pointer;
}
.faded{
  opacity: 0.9;
  border-radius: 10px;
}

.no-border{
  border-bottom-style: none !important;
  border-style: none;
}

</style>
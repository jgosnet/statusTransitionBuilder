<template lang="pug">
v-card(color="transparent" elevation="0" )
  SnackBarPopup
  v-layout
    v-app-bar(color="surface-variant" prominent density="compact" )
      v-menu(transition="slide-y-transition")
        template(v-slot:activator="{ props }")
          v-btn(v-bind="props" icon="fas fa-bars")
        v-list(density="compact" nav)
          v-list-item(v-for='item in menuItems'
            :key='item.title'
            :to='item.path'
            :prepend-icon="item.icon"
            exact-active-class='grey' large)
            v-list-item-title.item-title {{item.title}}

      v-toolbar-title
        v-icon fa-brands fa-youtube
        span.pl-3 Accurate launcher
        //v-spacer
      i.pr-4 updated on: 9/20/2023

  router-view(v-slot="{ Component }")
    transition(name="fade" mode="out-in" )
      keep-alive
        Component(:is="Component")


</template>

<script>
/* eslint-disable */
import './assets/main.css'
import SnackBarPopup from "@/components/utils/SnackBarPopup";
import {mapGetters} from "vuex";
import DpdBuilderPage from "@/components/DpdBuilderPage"

export default {
  name: 'App',
  components: {
    SnackBarPopup,
    DpdBuilderPage
  },
  data() {
    return {
      menuItems: [
        {title: 'DPD input', path: '/dpd', icon: 'fa-solid fa-indent'},
        {title: 'Preset builder', path: '/preset', icon: 'fa-solid fa-gears'},
      ]
    }
  },
    computed: {
    },
  methods: {
    openSnackbar(){
      this.snackbar = true
    },

  },
  mounted() {
    console.log('loading!')
    // this.$store.dispatch('configuration/loadConfiguration');
  }
}
</script>

<style>

.left-align{
  text-align: left;
}

.right-align{
  text-align: right;
}

body{
        /*background-image: url('/src/assets/background-2462431_1920.jpg') !important;*/
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: 100% 100%;
}
#app {
  font-family: Roboto;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 45px;


}

.default_height {
  padding-top: 0px;
  min-height: 300px;
}

.fade-enter-active {
  transition: all 0.2s ease-out;
}

.fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}

.fade-enter-from,
.fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

input[type=checkbox]{
     margin: 4px 0 0;
    line-height: normal;
    width: 20px;
    height: 20px;
}

fieldset{
min-height: 20px;
}

#expand{
  position: absolute;
  float:right;
  right: 20px;
  background-color: white;
  margin-top:-25px;
  margin-right:5px;
}

</style>

import {createRouter, createWebHistory} from "vue-router";
import DpdBuilderPage from "@/components/DpdBuilderPage";
import PresetBuilderPage from "@/components/PresetBuilderPage";

export const routes = [
  {
    path: '/dpd',
    component: DpdBuilderPage,
  },
  {
    path: '/preset',
    component: PresetBuilderPage,
  }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
});


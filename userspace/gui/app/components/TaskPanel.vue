<template>
  <div id="taskPanel">
  </div>
</template>

<script lang="ts">
// import libs
import { Component, Vue, Prop, Watch } from 'vue-property-decorator'
// import types
import { Equipment } from '@/types/Equipment'

@Component
export default class TaskPanel extends Vue {
  @Prop({ type: Object, required: false }) readonly equipped?: Equipment
}
</script>

<style scoped>
#taskPanel{
  flex-grow: 1;
  height: 100%;
  box-shadow: inset 0px 0px 30px 5px rgba(0, 0, 0, .5);
  background: rgba(255, 255, 255, .1);
}
</style>
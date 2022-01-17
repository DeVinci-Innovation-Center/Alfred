<template>
  <div id="taskPanel">
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'vue-property-decorator'

@Component
export default class TaskPanel extends Vue {
  @Prop({ type: Object, required: false }) readonly equipped?: Equipment
}
</script>

<style scoped>

</style>
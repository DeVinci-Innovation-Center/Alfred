<template>
  <div id="taskList">
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'vue-property-decorator'

@Component
export default class TaskList extends Vue {
  @Prop({ type: Object, required: false }) readonly equipped?: Equipment
}
</script>

<style scoped>

</style>
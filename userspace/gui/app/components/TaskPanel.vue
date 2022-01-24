<template>
  <div id="taskPanel">
    <component :is="taskScreen"></component>
  </div>
</template>

<script lang="ts">
// import libs
import { Component, Vue, Prop, Watch } from 'vue-property-decorator'
// import componentes
import HandTaskScreen from '@/components/taskScreen/HandTaskScreen.vue'
import PrintingNozzleTaskScreen from '@/components/taskScreen/PrintingNozzleTaskScreen.vue'
// import types
import { Equipment } from '@/types/Equipment'

@Component({
  components: {
    HandTaskScreen,
    PrintingNozzleTaskScreen
  }
})
export default class TaskPanel extends Vue {
  @Prop({ type: Object, required: false }) readonly equipped?: Equipment

  get taskScreen() {
    let task = ''
    if (this.equipped) {
      switch (this.equipped.name) {
        case 'hand':
          task = 'HandTaskScreen'
          break
        case 'fake 4':
          task = 'PrintingNozzleTaskScreen'
          break
      }
    }
    return task
  }
}
</script>

<style scoped>
#taskPanel {
  flex-grow: 1;
  height: 100%;
  padding: 15px 5px;
  box-shadow: inset 0px 0px 30px 5px rgba(0, 0, 0, 0.5);
  background: rgba(255, 255, 255, 0.1);
  overflow: hidden;
}
</style>

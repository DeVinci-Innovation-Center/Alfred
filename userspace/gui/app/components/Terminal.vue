<template>
  <div id="terminal">
    <div id="terminalLogs"></div>
    <input type="text" />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Watch } from 'vue-property-decorator'

@Component
export default class Terminal extends Vue {
  // @Prop({ type: Object, required: true }) readonly pose!: ArmPose
}
</script>

<style scoped>
#terminal {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 15vh;
  margin-top: 15px;
  overflow-y: scroll;
  background: rgba(0, 0, 0, .5);
  font-family: 'Source Code Pro', monospace;
  font-size: 1rem;
  overflow-x: hidden;
}
#terminalLogs{
  display: flex;
  flex-grow: 1;
}
#terminal input{
 text-align: left;
 margin: 4px;
}
</style>

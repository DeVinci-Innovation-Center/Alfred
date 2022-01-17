<template>
  <div id="equipmentBar" :class="`${clickedStop ? 'stopped' : ''}`">
    <span v-for="(eq, i) in equipments" :key="`equipment${i}`" :title="eq.name" @click="()=>{selectEquipment(i)}"></span>
  </div>
</template>

<script lang="ts">
// import libs
import { Component, Vue, Prop } from 'vue-property-decorator'
// import types
import { Equipment } from '@/types/Equipment'

@Component
export default class EquipmentBar extends Vue {
  @Prop({ type: Boolean, required: true }) readonly clickedStop!: boolean
  @Prop({ type: Object, required: false }) readonly equipped?: Equipment
  @Prop({ type: Array, required: true }) readonly equipments?: Equipment[]
}
</script>

<style scoped>
#equipmentBar {
  display: flex;
  align-self: center;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 50px;
}
#equipmentBar span {
  height: 20px;
  width: 20px;
  background: white;
  margin: 50px 0px;
  padding-left: 0px;
  cursor: pointer;
  box-shadow: 0px 0px 10px 5px white;
  transition: all .3s ease;
  position: relative;
}
#equipmentBar.stopped span {
  box-shadow: none;
  opacity: .5;
}
#equipmentBar span:hover{
  padding-left: 5px;
}
</style>

<template>
  <div
    v-if="scrolledEquip"
    id="taskListHolder"
    :class="clickedStop ? 'stopped' : ''"
  >
    <h3 id="equippedTitle" ref="equippedTitle">
      {{
        ` ${scrolledEquip.name} ${scrolledEquipmentIsActive ? '(active)' : ''}`
      }}
    </h3>
    <h3 style="font-size: 1.3rem; opacity: 0.7"><i>Available Tasks</i></h3>
    <ul :class="`${scrolledEquipmentIsActive ? 'currently-equipped' : ''}`">
      <li
        v-for="(task, i) in scrolledEquip.tasks"
        :key="`task-${i}`"
        :title="task.description"
        @click="
          () => {
            taskClick(i)
          }
        "
      >
        {{ task.name }}
        <font-awesome-icon :icon="['fas', 'play-circle']" />
      </li>
    </ul>
    <button
      id="equipButton"
      @click="
        () => {
          changeEquipment()
        }
      "
    >
      {{ scrolledEquipmentIsActive ? 'Unequip' : 'equip' }}
    </button>
  </div>
</template>

<script lang="ts">
// import libs
import { Component, Vue, Prop } from 'vue-property-decorator'
import '@fortawesome/fontawesome-free'
// import types
import { Equipment } from '../types/Equipment'
// import misc
import { EventBus } from '../utils/EventBus'

@Component
export default class TaskList extends Vue {
  @Prop({ type: Boolean, required: true }) readonly clickedStop!: boolean
  @Prop({ type: Object, required: false }) readonly equipped?: Equipment
  @Prop({ type: Object, required: false }) readonly scrolledEquip?: Equipment
  @Prop({ type: Array, required: true }) readonly equipments!: Equipment[]

  get scrolledEquipmentIsActive() {
    return (
      this.scrolledEquip &&
      this.equipped &&
      this.scrolledEquip.name === this.equipped.name
    )
  }

  changeEquipment() {
    const key = this.scrolledEquipmentIsActive
      ? -1
      : this.equipments.findIndex(
          (equi) => equi.name === this.scrolledEquip!.name
        )
    EventBus.$emit('change-equipment', key)
  }

  taskClick(i: number) {
    EventBus.$emit('doTask', this.equipped!.tasks[i])
  }
}
</script>

<style scoped>
#taskListHolder {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 13vw;
  background: rgba(15, 30, 40, 0.75);
}
#taskListHolder.stopped {
  pointer-events: none;
}
h3 {
  margin-top: 15px;
}
h3#equippedTitle {
  font-size: 1.5rem;
  padding-bottom: 15px;
  border-bottom: 1px solid white;
  text-transform: capitalize;
}
#equipButton {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-bottom-left-radius: 10px;
  width: 100%;
  padding: 10px 0px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 400;
  text-transform: uppercase;
}
#equipButton:hover {
  opacity: 0.75;
}
#taskListHolder ul {
  display: flex;
  flex-direction: column;
  align-items: center;
  pointer-events: none;
  opacity: 0.5;
  transition: all 0.3s ease;
  flex-grow: 1;
  padding-top: 20px;
  /* background: rgba(0, 255, 0, 0.5); */
}
#taskListHolder ul li {
  transition: all 0.3s ease;
  width: 90%;
  padding: 10px;
  text-align: left;
  font-size: 1.2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: transparent;
  cursor: pointer;
}
#taskListHolder ul li:hover {
  background: rgba(255, 255, 255, 0.1);
}
#taskListHolder ul li svg {
  font-size: 1.5rem;
}
#taskListHolder ul.currently-equipped {
  pointer-events: all;
  opacity: 1;
}
</style>

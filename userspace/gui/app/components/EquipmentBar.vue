<template>
  <div
    id="equipmentBar"
    :class="clickedStop ? 'stopped' : ''"
    @mousewheel="
      (e) => {
        scrollInput(e)
      }
    "
  >
    <div id="selectedCue">
      <hr />
      <hr />
    </div>
    <div id="equipmentHolder" ref="equipmentHolder">
      <div
        v-for="(eq, i) in equipments"
        :id="`${eq.name}-icon`"
        :key="`equipment-${i}`"
        class="icon"
        @click="
          () => {
            scrollEquipment(i)
          }
        "
      >
        <img
          :title="eq.name"
          :src="
            !eq.name.includes('fake')
              ? `/icons/${eq.name}-icon.png`
              : '/icons/fake-icon.png'
          "
          :alt="eq.name"
        />
        <span
          :class="`iconGlow ${
            equipped && equipped.name === eq.name ? 'active' : ''
          }`"
        ></span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
// import libs
import { Component, Vue, Prop, Watch } from 'vue-property-decorator'
import { gsap } from 'gsap'
// import types
import { Equipment } from '../types/Equipment'
// import misc
import { EventBus } from '../utils/EventBus'

@Component
export default class EquipmentBar extends Vue {
  @Prop({ type: Boolean, required: true }) readonly clickedStop!: boolean
  @Prop({ type: Object, required: false }) readonly equipped?: Equipment
  @Prop({ type: Object, required: false }) readonly scrolledEquip?: Equipment
  @Prop({ type: Array, required: true }) readonly equipments!: Equipment[]
  scrollDelay = 75 // miliseconds in-between equipment scrolls
  allowScroll = true

  mounted() {
    const middleIndex = Math.ceil(this.equipments.length/2)-1
    setTimeout(()=>{this.scrollEquipment(middleIndex)}, 250)
  }

  scrollEquipment(i: number) {
    EventBus.$emit('scroll-equipment', i)
  }

  @Watch('scrolledEquip')
  updateScrollEquipped() {
    // get DOM elements
    const holder = this.$refs.equipmentHolder as HTMLElement
    const key = `${this.scrolledEquip!.name}-icon`
    // compute
    const targetIcon = document.getElementById(key)!
    const targetOffset = holder.clientHeight / 2 - targetIcon.clientHeight / 2
    const currentOffset = targetIcon.offsetTop + holder.offsetTop
    const distance = targetOffset - currentOffset
    // animate
    gsap.to(holder, {
      duration: 0.35,
      top: `${holder.offsetTop + distance}px`
    })
  }

  scrollInput(e: WheelEvent) {
    if (this.allowScroll) {
      const index = this.equipments.findIndex(
        (equi) => equi.name === this.scrolledEquip!.name
      )
      if (e.deltaY > 0 && index < this.equipments.length - 1) {
        this.scrollEquipment(index + 1)
      } else if (e.deltaY < 0 && index > 0) {
        this.scrollEquipment(index - 1)
      }
      this.allowScroll = false
      setTimeout(() => {
        this.allowScroll = true
      }, this.scrollDelay)
    }
  }
}
</script>

<style scoped>
#equipmentBar {
  position: relative;
  display: flex;
  align-self: center;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 65px;
}
#equipmentBar.stopped {
  pointer-events: none;
}
#selectedCue {
  position: absolute;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 0;
  width: 100%;
  left: 0px;
}
#selectedCue hr {
  width: 100%;
  margin: 50px 0px;
  transition: all 0.3s ease;
  border-top: 1px solid white;
}
#equipmentHolder {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}
#equipmentHolder .icon {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}
#equipmentHolder img {
  margin: 40px 0px;
  padding-left: 0px;
  cursor: pointer;
  position: relative;
}
#equipmentBar .iconGlow {
  position: absolute;
  pointer-events: none;
  width: 35px;
  height: 35px;
  border-radius: 50px;
  background: radial-gradient(
    rgba(255, 255, 255, 0.5),
    transparent,
    transparent
  );
  transition: all 0.3s ease;
}
#equipmentBar .iconGlow.active {
  background: radial-gradient(rgba(255, 255, 255, 1), transparent);
  width: 50px;
  height: 50px;
}
#equipmentBar .icon:hover .iconGlow {
  box-shadow: 0px 0px 10px 5px rgba(255, 255, 255, 1);
}
</style>

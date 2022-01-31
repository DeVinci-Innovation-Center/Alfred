<template>
  <main>
    <div id="canvasHolder" ref="canvasHolder">
      <div
        id="currentlyResizing"
        ref="currentlyResizing"
        :class="`${
          (isDragging || clickedStop ? 'show ' : '') +
          (clickedStop ? 'red ' : '')
        }`"
      >
        {{ clickedStop ? 'STOPPED' : 'Resizing...' }}
        <img
          v-if="!clickedStop"
          src="/resize-icon.svg"
          alt="horizontal resize icon"
        />
      </div>
      <RenderCanvas
        :pose="currentPose"
        :clicked-stop="clickedStop"
        :equipped="equipped"
        :watching="watching"
        :style="`filter:grayscale(${status == 'offline' ? 1 : 0})`"
      />
    </div>
    <div id="dashboardWrapper" ref="dashboardWrapper">
      <!-- OVERLAYED INPUT -->
      <span id="border" ref="border"></span>
      <img
        id="infoIcon"
        ref="infoIcon"
        src="/info-icon.svg"
        alt="information icon"
        :style="`filter: invert(${infoPanelIsOpen ? 1 : 0})`"
        @click="
          () => {
            infoClick()
          }
        "
      />
      <div id="infoPanelHolder" :class="`${infoPanelIsOpen ? 'show' : ''}`">
        <InfoPanel />
      </div>
      <!-- RELATIVE ELEMENTS -->
      <div style="display: flex; flex-grow: 1; overflow-y: hidden">
        <EquipmentBar
          v-if="equipments.length"
          :equipments="equipments"
          :clicked-stop="clickedStop"
          :equipped="equipped"
          :scrolled-equip="scrolledEquip"
        />
        <div id="dashboard">
          <!-- DASHBOARD HEADER -->
          <div id="dashboardHeader">
            <h1 :class="`${clickedStop ? 'stopped' : ''}`">
              Alfred is <span>{{ status }}</span>
            </h1>
          </div>

          <!-- MAIN DASHBOARD CONTENT -->
          <div id="dashboardBody">
            <div id="dashboardMain">
              <JointGauges
                :current-pose="currentPose"
                :clicked-stop="clickedStop"
                :watching="watching"
              />
              <div id="taskManager">
                <TaskList
                  v-if="equipments.length"
                  :equipments="equipments"
                  :equipped="equipped"
                  :scrolled-equip="scrolledEquip"
                  :clicked-stop="clickedStop"
                />
                <TaskPanel :equipped="equipped" :clicked-stop="clickedStop" />
              </div>
            </div>
            <EmergencyStopBtn
              :clicked-stop="clickedStop"
              :status="status"
              @click="
                () => {
                  emergencyStop()
                }
              "
            />
          </div>
        </div>
      </div>
      <ArmOutline :clicked-stop="clickedStop" />
      <div id="terminalHolder">
        <!-- <Terminal /> -->
      </div>
    </div>
  </main>
</template>

<script lang="ts">
// import libs
import { Component, Vue } from 'vue-property-decorator'
import { io, Socket } from 'socket.io-client'
import { gsap } from 'gsap'
// import components
import RenderCanvas from '../components/RenderCanvas.vue'
import InfoPanel from '../components/InfoPanel.vue'
import JointGauges from '../components/JointGauges.vue'
import EquipmentBar from '../components/EquipmentBar.vue'
import TaskList from '../components/TaskList.vue'
import TaskPanel from '../components/TaskPanel.vue'
import EmergencyStopBtn from '../components/EmergencyStopBtn.vue'
import ArmOutline from '../components/ArmOutline.vue'
import Terminal from '../components/Terminal.vue'
// import types
import { ArmPose } from '../types/ArmPose'
import { Equipment, Task } from '../types/Equipment'
// import misc
import { EventBus } from '../utils/EventBus'

@Component({
  components: {
    RenderCanvas,
    InfoPanel,
    JointGauges,
    EquipmentBar,
    TaskList,
    TaskPanel,
    EmergencyStopBtn,
    ArmOutline,
    Terminal
  }
})
export default class Index extends Vue {
  socketTarget = process.env.socketTarget!
  io!: Socket
  currentPose: ArmPose = {
    joint_1: 0,
    joint_2: -1,
    joint_3: -.6,
    joint_4: 0,
    joint_5: 0,
    joint_6: 0,
    head: { equipment: null }
  }

  watching = false
  equipments: Equipment[] = []
  equipped?: Equipment | null = null
  scrolledEquip?: Equipment | null = null
  currentTask?: Task | null = null
  clickedStop = false
  infoPanelIsOpen = false
  isDragging = false
  status = 'online'

  created() {
    console.log('this.socketTarget : ', this.socketTarget)
  }

  async mounted() {
    // this.io.on('arm-pose', (data) => {
    //   gsap.to(this.currentPose, {
    //     duration: 0.5,
    //     joint_1: data.joint_1,
    //     joint_2: data.joint_2,
    //     joint_3: data.joint_3,
    //     joint_4: data.joint_4,
    //     joint_5: data.joint_5,
    //     joint_6: data.joint_6,
    //     head: data.head
    //   })
    // })
    // this.io.on('return-configuration', (data:any)=>{
    //   this.equipments = data.equipments as Equipment[]
    // })
    // this.io.on('status-change', (data:any)=>{
    //   this.status = data.status
    // })

    // to erase when io is on
    setInterval(() => {
      if (!this.clickedStop) {
        this.currentPose = {
          joint_1: (this.currentPose.joint_1 + 0.01) % (Math.PI * 2),
          joint_2: this.currentPose.joint_2,
          joint_3: this.currentPose.joint_3,
          joint_4: (this.currentPose.joint_4 + 0.02) % (Math.PI * 2),
          joint_5: this.currentPose.joint_5,
          joint_6: this.currentPose.joint_6,
          head: { equipment: null }
        }
      }
    }, 20)

    this.equipments =
      (await require('@/assets/fake_equipments.json')) as Equipment[]

    this.setDragResizer()

    EventBus.$on('emergency-stop', () => {
      // this.io.emit('emergency-stop')
      this.clickedStop = true
      this.status = 'stopping'
    })
    EventBus.$on('change-equipment', (i: number) => {
      if (i < 0) {
        this.equipped = null
        // this.io.emit('change-equipment', null)
      } else {
        this.equipped = this.equipments[i]
        // this.io.emit('change-equipment', this.equipments[i].name)
      }
    })
    EventBus.$on('scroll-equipment', (i: number) => {
      if (i < 0) {
        this.scrolledEquip = null
      } else {
        this.scrolledEquip = this.equipments[i]
      }
    })
    EventBus.$on('toggle-watching', () => {
      this.watching = !this.watching
    })
  }

  setDragResizer() {
    const border = this.$refs.border as HTMLElement
    const left = this.$refs.canvasHolder as HTMLElement
    const right = this.$refs.dashboardWrapper as HTMLElement

    // toggle drag behaviour
    border.addEventListener('mousedown', () => {
      this.isDragging = true
      border.style.background = 'white'
    })
    document.body.addEventListener('mouseup', () => {
      this.isDragging = false
      border.style.background = 'transparent'
    })

    // defining drag behaviour
    window.addEventListener('mousemove', (e) => {
      if (this.isDragging) {
        e.preventDefault()
        const ratio = e.x / window.innerWidth
        left.style.flexGrow = ratio.toString()
        right.style.flexGrow = (1 - ratio).toString()
        EventBus.$emit('resize')
      }
    })

    // safeguard
    document.addEventListener('mouseenter', () => {
      this.isDragging = false
    })
  }

  infoClick() {
    this.infoPanelIsOpen = !this.infoPanelIsOpen
  }
}
</script>

<style scoped>
#canvasHolder,
#dashboardWrapper {
  position: relative;
  display: flex;
  width: 0px;
  flex-grow: 0.5;
}
#dashboardWrapper {
  display: flex;
  flex-direction: column;
}
#currentlyResizing {
  position: absolute;
  z-index: 99;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(15, 30, 40, 0.8);
  font-size: 3rem;
  opacity: 0;
  pointer-events: none;
  transition: all 0.4s ease;
}
#currentlyResizing.show {
  opacity: 1;
}
#currentlyResizing.red {
  background: rgba(80, 0, 0, 0.75);
}
#currentlyResizing img {
  width: 150px;
  animation: 2s linear infinite both resizing;
}
@keyframes resizing {
  0% {
    margin-left: 0px;
  }
  25% {
    margin-left: 50px;
  }
  75% {
    margin-left: -50px;
  }
}

/* 
----------------
    DASHBOARD
----------------
*/
#dashboard {
  position: relative;
  display: flex;
  flex-grow: 1;
  /* width: 100%; */
  /* width: 100%; */
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  /* border: 2px solid red; */
  overflow: hidden;
}
#border {
  position: absolute;
  z-index: 99;
  height: 100%;
  width: 0.2vw;
  left: -0.2vw;
  cursor: col-resize;
}
#infoIcon {
  width: 40px;
  position: absolute;
  z-index: 99;
  top: 10px;
  right: 10px;
  transition: all 0.3s ease;
  cursor: pointer;
}
#infoIcon:hover {
  opacity: 0.5;
}
#infoPanelHolder {
  position: absolute;
  z-index: 90;
  height: 100%;
  width: 100%;
  overflow: hidden;
  pointer-events: none;
}
#infoPanel {
  position: absolute;
  height: 100%;
  width: 100%;
  background: white;
  font-family: 'DDINExp';
  color: black;
  right: -100%;
  transition: all 0.3s ease;
  pointer-events: all;
}
#infoPanelHolder.show #infoPanel {
  right: 0%;
}
/* ---------
    HEADER 
-----------*/
#dashboardHeader {
  margin-top: 20px;
  width: 100%;
}
h1 {
  font-size: 3.5rem;
  font-family: 'Roboto', sans-serif;
  text-align: left;
}
#dashboardHeader h1 span {
  font-family: 'Source Code Pro', monospace;
  background: rgba(0, 0, 0, 0.4);
  padding: 0px 8px;
  border-radius: 10px;
  box-shadow: inset 0px 0px 15px 5px rgba(0, 0, 0, 0.5);
}
#dashboardHeader h1.stopped span {
  background: rgba(150, 0, 0, 0.4);
}
/* ---------
    BODY 
-----------*/
#dashboardBody {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  flex-grow: 1;
  /* border: 1px solid green; */
}
#dashboardMain {
  display: flex;
  flex-grow: 1;
  width: 100%;
  flex-direction: column;
  align-items: center;
  /* border: 1px solid white; */
}
#taskManager {
  background: rgba(0, 0, 0, 0.65);
  flex-grow: 1;
  width: 95%;
  margin: 10px 0px;
  border-radius: 10px;
  display: flex;
  overflow: hidden;
}
#emergencyStopBtn {
  font-size: 2rem;
  /* border: 1px solid white; */
  border-radius: 10px;
  padding: 8px;
  cursor: pointer;
  width: fit-content;
}
/* #terminalHolder{
  display: flex;
  align-self: flex-end;
  width: 100vw; 
}*/
</style>

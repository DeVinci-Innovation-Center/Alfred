<template>
  <div id="handScreen">
    <div id="sliderLabels">
      <span>00.00</span>
      <h3 id="currentOpening">
        {{ (currentOpeningRatio * 85).toFixed(2) }} mm
      </h3>
      <span>85.00</span>
    </div>
    <div id="sliderHolder">
      <span id="sliderRange"></span>
      <span
        id="sliderCursor"
        :style="`left:calc(${currentOpeningRatio * 100}% - 10px`"
      ></span>
    </div>
    <span id="caption">current opening</span>
    <hr />
    <div v-if="scanning" id="scanningHolder">
      <font-awesome-icon id="scanLoader" :icon="['fas', 'circle-notch']" />
      <span>Scanning...</span>
    </div>
    <div
      id="scannedHolder"
      ref="scannedHolder"
      :style="`visibility:${scanned ? 'visible' : 'hidden'}`"
    ></div>
  </div>
</template>

<script lang="ts">
// import libs
import { Component, Vue } from 'vue-property-decorator'
import { gsap, Linear } from 'gsap'
import * as echarts from 'echarts'
import 'echarts-gl'
// import types
import { Equipment, Task } from '../../types/Equipment'
// import misc
import { EventBus } from '../../utils/EventBus'

@Component
export default class HandTaskScreen extends Vue {
  currentOpeningRatio = 0
  tweenDuration = 2
  bltChart!: echarts.ECharts
  scanning = false
  scanned = false

  mounted() {
    EventBus.$on('doTask', (task: Task) => {
      switch (task.name.toLowerCase()) {
        case 'open':
          gsap.to(this, {
            duration: this.tweenDuration,
            currentOpeningRatio: 1,
            ease: Linear.easeNone
          })
          break
        case 'close':
          gsap.to(this, {
            duration: this.tweenDuration,
            currentOpeningRatio: 0,
            ease: Linear.easeNone
          })
          break
        case 'blt scan':
          this.launchBLTScan()
          break
        default:
          break
      }
    })
  }

  launchBLTScan() {
    this.scanning = true

    /** INITIALIZE SCATTER GRAPH **/

    const container = this.$refs.scannedHolder as HTMLElement
    console.log(container) // ???
    // initialize the echarts instance
    this.bltChart = echarts.init(container, undefined, {
      width: container.clientWidth,
      height: container.clientHeight
    })
    // Draw the chart
    const data = []
    for (let x = -20; x < 20; x++) {
      for (let y = -20; y < 20; y++) {
        data.push([x * 2, y * 2, 0])
      }
    }
    this.bltChart.setOption({
      tooltip: { show: false },
      silent: true,
      grid3D: {},
      xAxis3D: {
        name: 'X (cm)',
        min: -50,
        max: 50,
        nameGap: 25,
        nameTextStyle: { color: 'white' }
      },
      yAxis3D: {
        name: 'Y (cm)',
        min: -50,
        max: 50,
        nameGap: 25,
        nameTextStyle: { color: 'white' }
      },
      zAxis3D: {
        name: 'Z (cm)',
        min: 0,
        max: 100,
        nameGap: 25,
        nameTextStyle: { color: 'white' }
      },
      axisTick: { lineStyle: { color: 'white' } },
      axisLabel: { color: 'white' },
      dataset: {
        dimensions: [],
        source: data
      },
      series: [
        {
          type: 'scatter3D',
          symbolSize: 3,
          symbol: 'circle',
          color: 'white',
          emphasis: { scale: false }
        }
      ]
    })

    // resize gauges when needed
    const resizeGraph = () => {
      this.bltChart.resize({
        width: container.clientWidth,
        height: container.clientHeight
      })
      console.log('resize to : ', container.clientWidth)
    }
    EventBus.$on('resize', resizeGraph)
    window.addEventListener('resize', resizeGraph)
    setTimeout(resizeGraph, 10) // ugly but needed for first load

    setTimeout(() => {
      this.scanning = false
      this.scanned = true
      this.updateGraph()
    }, 3000)
  }

  updateGraph() {
    const data = []
    for (let x = -20; x < 20; x++) {
      for (let y = -20; y < 20; y++) {
        let myZ = 0
        if (x < 15 && y > 17) {
          myZ += 10
        } else if (x < 13 && y > 16) {
          myZ += 8
        } else if (x < 13 && y > 16) {
          myZ += 8
        } else if (x < 5 && x > -3 && y < 5) {
          myZ += 5
        } else if (x < 6 && x > -4 && y < 6) {
          myZ += 2
        } else if (x < -10 && y < -15) {
          myZ += 25
        } else if (x > -12 && x < -10 && y > -5 && y < 5) {
          myZ += 2
        }
        data.push([x * 2, y * 2, myZ])
      }
    }

    const options = {
      grid3D: {},
      xAxis3D: { name: 'X (cm)', min: -50, max: 50 },
      yAxis3D: { name: 'Y (cm)', min: -50, max: 50 },
      zAxis3D: { name: 'Z (cm)', min: 0, max: 100 },
      dataset: {
        dimensions: [],
        source: data
      },
      series: [
        {
          type: 'scatter3D',
          symbolSize: 3,
          symbol: 'circle',
          color: 'white'
        }
      ]
    }
    this.bltChart.setOption(options)
  }
}
</script>

<style scoped>
#handScreen {
  display: flex;
  flex-direction: column;
  align-items: center;
  align-self: center;
  justify-content: center;
  height: 100%;
}
#sliderHolder {
  position: relative;
  display: flex;
  align-items: center;
  width: 90%;
  height: 20px;
  margin: 5px 0px;
}
#sliderRange {
  background: rgba(190, 210, 255, 0.4);
  width: 100%;
  height: 50%;
  border-radius: 100px;
}
#sliderLabels {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
#sliderCursor {
  background: rgba(190, 210, 255, 0.95);
  height: 20px;
  width: 20px;
  transform: rotate(45deg);
  position: absolute;
  left: auto;
}
#currentOpening {
  font-size: 2.5rem;
}
hr {
  height: 0px;
  width: 90%;
  border-top: 1px solid rgba(255, 255, 255, 0.25);
  margin: 10px;
}
#scanningHolder {
  position: absolute;
  pointer-events: none;
  z-index: 10;
  top: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}
#scanningHolder {
  font-size: 2.5rem;
}
#scanLoader {
  font-size: 6rem;
  margin: 80px 30px 20px 30px;
  animation: 1s linear infinite spinScan;
}
@keyframes spinScan {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
#scannedHolder {
  width: 100%;
  flex-grow: 1;
}
</style>

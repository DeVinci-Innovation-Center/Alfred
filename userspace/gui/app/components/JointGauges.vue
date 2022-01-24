<template>
  <div id="jointGauges" ref="jointGauges">
    <div
      v-if="!clickedStop"
      id="watchToggler"
      @click="
        (e) => {
          toggleWatcher(e)
        }
      "
    >
      {{ watching ? 'Stop watching arm-pose' : 'Start watching arm-pose' }}
    </div>
    <div id="gaugesHolder" ref="gaugesHolder"></div>
  </div>
</template>

<script lang="ts">
// import libs
import { Component, Vue, Prop, Watch } from 'vue-property-decorator'
import * as echarts from 'echarts'
// import types
import { ArmPose } from '@/types/ArmPose'
// import misc
import { EventBus } from '@/utils/EventBus'
@Component
export default class JointGauges extends Vue {
  @Prop({ type: Object, required: true }) readonly currentPose!: ArmPose
  @Prop({ type: Boolean, required: true }) readonly clickedStop!: boolean
  @Prop({ type: Boolean, required: true }) readonly watching!: boolean
  jointsChart!: echarts.ECharts
  gaugeData = [
    [
      {
        value: 0,
        name: 'Joint 1',
        detail: {
          valueAnimation: true,
          offsetCenter: ['0%', '5%']
        }
      }
    ],
    [
      {
        value: 0,
        name: 'Joint 2',
        detail: {
          valueAnimation: true,
          offsetCenter: ['0%', '5%']
        }
      }
    ],
    [
      {
        value: 0,
        name: 'Joint 3',
        detail: {
          valueAnimation: true,
          offsetCenter: ['0%', '5%']
        }
      }
    ],
    [
      {
        value: 0,
        name: 'Joint 4',
        detail: {
          valueAnimation: true,
          offsetCenter: ['0%', '5%']
        }
      }
    ],
    [
      {
        value: 0,
        name: 'Joint 5',
        detail: {
          valueAnimation: true,
          offsetCenter: ['0%', '5%']
        }
      }
    ],
    [
      {
        value: 0,
        name: 'Joint 6',
        detail: {
          valueAnimation: true,
          offsetCenter: ['0%', '5%']
        }
      }
    ]
  ]

  mounted() {
    const container = this.$refs.gaugesHolder as HTMLElement
    // initialize the echarts instance
    this.jointsChart = echarts.init(container, undefined, {
      width: container.clientWidth,
      height: Math.min(container.clientWidth / 5, container.clientHeight)
    })

    // Draw the chart
    this.jointsChart.setOption({
      tooltip: { show: false },
      silent: true,
      series: this.initGaugeSeries()
    })

    // resize gauges when needed
    const resizeGauges = () => {
      this.jointsChart.resize({
        width: container.clientWidth,
        height: Math.min(container.clientWidth / 5, container.clientHeight)
      })
    }
    EventBus.$on('emergency-stop', () => {
      this.updateGaugeSeries()
    })
    EventBus.$on('resize', resizeGauges)
    window.addEventListener('resize', resizeGauges)
    setTimeout(resizeGauges, 10) // ugly but needed for first load
  }

  initGaugeSeries() {
    const series = []
    for (let i = 0; i < 6; i++) {
      series.push({
        center: [`${8.3 + 16.7 * i}%`, '45%'],
        type: 'gauge',
        startAngle: -90,
        endAngle: -450,
        pointer: {
          show: false
        },
        animation: false,
        legendHoverLink: false,
        progress: {
          show: true,
          overlap: false,
          roundCap: true,
          clip: false,
          itemStyle: {
            borderWidth: 0,
            borderColor: '#464646',
            color: 'white',
            shadowColor: 'white',
            shadowBlur: 10
          }
        },
        axisLine: {
          lineStyle: {
            width: 6,
            color: [[10, 'black']]
          }
        },
        splitLine: {
          show: false,
          distance: 0,
          length: 10
        },
        axisTick: {
          show: true,
          distance: 6,
          length: 4,
          splitNumber: 3
        },
        axisLabel: {
          show: false,
          distance: 50
        },
        data: this.gaugeData[i],
        title: {
          offsetCenter: ['0%', '130%'],
          color: 'white',
          fontSize: 15
        },
        detail: {
          width: 50,
          height: 14,
          fontSize: 12,
          color: 'white',
          borderWidth: 0,
          formatter: (value: number) => `${(value / 50).toFixed(2)} rad`
        }
      })
    }
    return series
  }

  @Watch('currentPose')
  @Watch('clickedStop')
  updateGaugeSeries() {
    if (this.watching || this.clickedStop) {
      const series = []
      for (let i = 0; i < 6; i++) {
        const rotation = Object.values(this.currentPose)[i]
        this.gaugeData[i][0].value = (rotation / (Math.PI * 2)) * 100
        series.push({
          data: this.gaugeData[i],
          pointer: {
            show: false
          },
          progress: {
            itemStyle: {
              color: this.clickedStop ? 'rgba(255, 0, 0, .4)' : 'white',
              shadowColor: this.clickedStop ? 'rgba(255, 0, 0, .4)' : 'white'
            }
          }
        })
      }
      this.jointsChart.setOption({ series })
    }
  }

  toggleWatcher(e: MouseEvent) {
    e.preventDefault()
    EventBus.$emit('toggle-watching')
  }
}
</script>

<style scoped>
#jointGauges {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 150px;
  margin: 10px 0px;
  justify-content: space-around;
  /* border: 1px solid blue; */
}
#gaugesHolder {
  height: 100%;
  width: 100%;
}
#watchToggler {
  position: absolute;
  z-index: 5;
  height: 100%;
  width: 100%;
  font-size: 3rem;
  font-weight: 400;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  background: rgba(0, 0, 0, 0.75);
  border-radius: 10px;
  transition: all 0.3s ease;
  opacity: 0;
}
#watchToggler:hover {
  opacity: 0.85;
}
</style>

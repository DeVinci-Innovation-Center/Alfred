<template>
  <div id="jointGauges" ref="jointGauges">
    <span id="stop">STOP !</span>
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
  myChart!: echarts.ECharts
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
    const container = this.$refs.jointGauges as HTMLElement
    // initialize the echarts instance
    this.myChart = echarts.init(container, undefined, {
      width: container.clientWidth,
      height: Math.min(container.clientWidth / 5, container.clientHeight)
    })

    // Draw the chart
    this.myChart.setOption({
      tooltip: { show: false },
      silent: true,
      series: this.initGaugeSeries()
    })

    // resize gauges when needed
    const resizeGauges = () => {
      this.myChart.resize({
        width: container.clientWidth,
        height: Math.min(container.clientWidth / 5, container.clientHeight)
      })
    }
    EventBus.$on('emergency-stop', () => {
      this.updateGaugeSeries()
    })
    EventBus.$on('resize', resizeGauges)
    window.addEventListener('resize', resizeGauges)
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

    this.myChart.setOption({ series })
  }
}
</script>

<style scoped>
#jointGauges {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 150px;
  justify-content: space-around;
  /* border: 1px solid blue; */
}
#stop {
  position: absolute;
}
</style>

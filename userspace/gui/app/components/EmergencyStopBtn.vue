<template>
  <div
    id="EmergencyStopWrapper"
    :style="`${clickedStop && 'border-color: transparent !important;'}`"
    @mouseenter="
      () => {
        btnEnter()
      }
    "
    @mouseout="
      () => {
        btnOut()
      }
    "
    @click="
      () => {
        btnStopClick()
      }
    "
  >
    <div id="EmergencyStopChart" ref="EmergencyStopChart"></div>
    <span :class="`disable-select ${clickedStop && 'clickedStop'}`"> STOP</span>
  </div>
</template>

<script lang="ts">
// import libs
import { Component, Vue, Watch } from 'vue-property-decorator'
import * as echarts from 'echarts'
// import misc
import { EventBus } from '@/utils/EventBus'

@Component
export default class EmergencyStopBtn extends Vue {
  myChart!: echarts.ECharts
  clickedStop = false
  ringData = [
    {
      value: 0
    },
    {
      value: 0
    },
    {
      value: 0
    }
  ]

  ringSeries = {
    type: 'gauge',
    startAngle: 90,
    endAngle: -270,
    pointer: {
      show: false
    },
    radius: '100%',
    progress: {
      show: true,
      overlap: false,
      roundCap: true,
      clip: false,
      itemStyle: {
        borderWidth: 0,
        color: 'transparent'
      }
    },
    axisLine: {
      lineStyle: {
        width: 8,
        color: [[1, 'transparent']]
      }
    },
    splitLine: {
      show: false
    },
    axisTick: {
      show: false
    },
    axisLabel: {
      show: false
    },
    data: this.ringData,
    detail: {
      show: false
    }
  }

  sunStyle1 = {
    color: 'rgba(255, 255, 255, 1)'
  }

  sunStyle2 = {
    color: 'rgba(255, 255, 255, .8)'
  }

  sunStyle3 = {
    color: 'rgba(255, 255, 255, .3)'
  }

  sunData = [
    {
      children: [
        {
          value: 4,
          children: [
            {
              value: 1,
              itemStyle: this.sunStyle1
            },
            {
              value: 2,
              children: [
                {
                  value: 1,
                  itemStyle: this.sunStyle2
                }
              ]
            },
            {
              children: [
                {
                  value: 1
                }
              ]
            }
          ],
          itemStyle: this.sunStyle1
        }
      ],
      itemStyle: this.sunStyle1
    }
  ]

  sunSeries = {
    radius: ['50%', '80%'],
    type: 'sunburst',
    sort: undefined,
    data: this.sunData,
    label: {
      rotate: 'radial'
    },
    levels: [],
    itemStyle: {
      opacity: 0.1,
      color: this.sunStyle1,
      borderColor: 'rgb(15, 30, 40)',
      borderWidth: 3
    }
  }

  mounted() {
    const container = this.$refs.EmergencyStopChart as HTMLElement
    // initialize the echarts instance
    this.myChart = echarts.init(container, undefined, {
      width: container.clientWidth,
      height: container.clientWidth
    })

    // Draw the chart
    this.myChart.setOption({
      tooltip: { show: false },
      silent: true,
      series: [this.ringSeries, this.sunSeries]
    })
  }

  sunDataUnfolded(
    style1: { color: string },
    style2: { color: string },
    style3: { color: string }
  ) {
    return [
      {
        children: [
          {
            value: 1,
            children: [
              {
                value: 1,
                itemStyle: style1
              },
              {
                value: 2,
                children: [
                  {
                    value: 1,
                    itemStyle: style2
                  }
                ]
              },
              {
                children: [
                  {
                    value: 1
                  }
                ]
              }
            ],
            itemStyle: style1
          },
          {
            value: 10,
            children: [
              {
                value: 6,
                children: [
                  {
                    value: 1,
                    itemStyle: style1
                  },
                  {
                    value: 1
                  },
                  {
                    value: 1,
                    itemStyle: style2
                  },
                  {
                    value: 1
                  }
                ],
                itemStyle: style3
              },
              {
                value: 2,
                children: [
                  {
                    value: 1
                  }
                ],
                itemStyle: style3
              },
              {
                children: [
                  {
                    value: 1,
                    itemStyle: style2
                  }
                ]
              }
            ],
            itemStyle: style1
          }
        ],
        itemStyle: style1
      },
      {
        value: 9,
        children: [
          {
            value: 4,
            children: [
              {
                value: 2,
                itemStyle: style2
              },
              {
                children: [
                  {
                    value: 1,
                    itemStyle: style1
                  }
                ]
              }
            ],
            itemStyle: style1
          },
          {
            children: [
              {
                value: 3,
                children: [
                  {
                    value: 1
                  },
                  {
                    value: 1,
                    itemStyle: style2
                  }
                ]
              }
            ],
            itemStyle: style3
          }
        ],
        itemStyle: style2
      },
      {
        value: 7,
        children: [
          {
            children: [
              {
                value: 1,
                itemStyle: style3
              },
              {
                value: 3,
                children: [
                  {
                    value: 1,
                    itemStyle: style2
                  },
                  {
                    value: 1,
                    itemStyle: style2
                  }
                ],
                itemStyle: style2
              },
              {
                value: 2,
                children: [
                  {
                    value: 1,
                    itemStyle: style2
                  },
                  {
                    value: 1,
                    itemStyle: style1
                  }
                ],
                itemStyle: style1
              }
            ],
            itemStyle: style3
          }
        ],
        itemStyle: style1
      },
      {
        children: [
          {
            value: 6,
            children: [
              {
                value: 1,
                itemStyle: style2
              },
              {
                value: 2,
                children: [
                  {
                    value: 2,
                    itemStyle: style2
                  }
                ],
                itemStyle: style1
              },
              {
                value: 1,
                itemStyle: style3
              }
            ],
            itemStyle: style3
          },
          {
            value: 3,
            children: [
              {
                value: 1
              },
              {
                children: [
                  {
                    value: 1,
                    itemStyle: style2
                  }
                ]
              },
              {
                value: 1
              }
            ],
            itemStyle: style3
          }
        ],
        itemStyle: style1
      },
      {
        children: [
          {
            value: 1,
            children: []
          },
          {
            value: 2,
            itemStyle: style1,
            children: [
              {
                value: 2,
                children: [
                  {
                    value: 2,
                    itemStyle: style3
                  }
                ]
              }
            ]
          }
        ],
        itemStyle: style2
      }
    ]
  }

  btnEnter() {
    if (!this.clickedStop) {
      this.ringData[0].value = 75
      this.ringData[1].value = 100
      this.ringData[2].value = 90
      const series = [
        {
          data: this.ringData,
          pointer: {
            show: false
          },
          progress: {
            itemStyle: {
              color: 'white'
            }
          }
        },
        {
          radius: ['50%', '90%'],
          data: this.sunDataUnfolded(
            this.sunStyle1,
            this.sunStyle2,
            this.sunStyle3
          ),
          itemStyle: {
            opacity: 0.4
          }
        }
      ]
      this.myChart.setOption({ series })
    }
  }

  btnOut() {
    if (!this.clickedStop) {
      this.ringData[0].value = 0
      this.ringData[1].value = 0
      this.ringData[2].value = 0
      const series = [
        {
          data: this.ringData,
          pointer: {
            show: false
          },
          progress: {
            itemStyle: {
              color: 'transparent'
            }
          }
        },
        {
          radius: ['25%', '65%'],
          data: this.sunData,
          itemStyle: {
            opacity: 0.1
          }
        }
      ]
      this.myChart.setOption({ series })
    }
  }

  btnStopClick() {
    this.sunStyle1 = {
      color: 'rgba(200, 0, 0, 1)'
    }
    this.sunStyle2 = {
      color: 'rgba(200, 0, 0, .8)'
    }
    this.sunStyle3 = {
      color: 'rgba(200, 0, 0, .3)'
    }
    this.myChart.setOption({
      series: [
        {
          progress: {
            itemStyle: { color: 'rgba(255, 0, 0, .75' }
          }
        },
        {
          itemStyle: { color: 'rgba(255, 0, 0, 1)' },
          data: this.sunDataUnfolded(
            this.sunStyle1,
            this.sunStyle2,
            this.sunStyle3
          )
        }
      ]
    })
    this.clickedStop = true
    EventBus.$emit('emergency-stop')
  }
}
</script>

<style scoped>
#EmergencyStopWrapper {
  position: relative;
  height: 180px;
  width: 180px;
  border: 2px solid white;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer !important;
  transition: all 0.5s ease;
  border-radius: 100px;
}
#EmergencyStopChart {
  height: 100%;
  width: 100%;
  cursor: inherit;
  pointer-events: none;
}
#EmergencyStopWrapper span {
  position: absolute;
  font-size: 2.5rem;
  pointer-events: none;
  transition: all 0.35s ease;
  font-weight: 400;
}

#EmergencyStopWrapper span.clickedStop {
  color: red;
  transform: scale(0.8);
}

#EmergencyStopWrapper:hover span {
  transform: scale(0.8);
}
#EmergencyStopWrapper:hover {
  border-color: transparent;
}
</style>

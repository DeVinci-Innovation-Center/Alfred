<template>
  <main>
    <header>
      <h1>ALFRED's DASHBOARD</h1>
    </header>
    <RenderCanvas :pose="targetPose" />
  </main>
</template>

<script lang="ts">
// libs
import { Component, Vue } from 'vue-property-decorator'
import { io, Socket } from 'socket.io-client'
import { gsap } from 'gsap'
// components
import RenderCanvas from '@/components/RenderCanvas.vue'
// types
import { ArmPose } from '@/types/ArmPose'

@Component({
  components: {
    RenderCanvas,
  },
})
export default class Index extends Vue {
  socketTarget = process.env.socketTarget!
  io!: Socket
  targetPose: ArmPose = {
    joint_1: 0.017956436942507398,
    joint_2: -0.9737956905041772,
    joint_3: -0.7701755099417158,
    joint_4: -0.10276360990249185,
    joint_5: 1.6879406729438893,
    joint_6: -0.04612139081680539,
    module: -1,
  }

  created() {
    this.io = io(this.socketTarget)
  }

  mounted() {
    this.io.on(process.env.socketEventName!, (data) => {
      // this.targetPose = data.pose
      gsap.to(this.targetPose, {
        duration: 0.5,
        joint_1: data.pose.joint_1,
        joint_2: data.pose.joint_2,
        joint_3: data.pose.joint_3,
        joint_4: data.pose.joint_4,
        joint_5: data.pose.joint_5,
        joint_6: data.pose.joint_6,
        module: -1,
      })
    })

    // document.addEventListener(
    //   'keydown',
    //   (_event) => {

    //   },
    //   false
    // )
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700;900&display=swap');
body {
  background: rgb(230, 230, 230);
  font-family: 'Roboto', sans-serif;
  font-weight: 100;
  font-size: 5rem;
  text-align: center;
}
</style>

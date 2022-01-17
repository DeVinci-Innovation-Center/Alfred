<template>
  <article id="infoPanel">
    <h2>The ALFRED Project</h2>
    <p>
      This dashboard is the front-end of the Alfred project, a software
      interface used in various applications to drive a robotic arm called
      `X-Arm-6`. These include 3D printing, writing, grabbing objects, scanning
      environment, and obeying to voice or visual instructions.
    </p>
    <p>
      Alfred is an ongoing project of the Artificial Lives group, at the De
      Vinci Innovation Center. The links below list some related resources about
      the lab, the project, the device and source code.
    </p>
    <p><b>References :</b></p>
    <p>
      <a
        href="https://github.com/DeVinci-Innovation-Center/Alfred"
        target="_blank"
        >Project repository on github</a
      >
    </p>
    <p>
      <a href="https://dvic.devinci.fr/projects/xarm-bench" target="_blank"
        >Project page at dvic.devinci.fr</a
      >
    </p>
    <p>
      <a href="https://youtu.be/6KcHh4nWJFI" target="_blank"
        >Project video on youtube</a
      >
    </p>
    <span id="rights">Owned by the DVIC, made by Faber Smythe, 2022</span>
  </article>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class InfoPanel extends Vue {
  // @Prop({ type: Object, required: true }) readonly pose!: ArmPose
}
</script>

<style scoped>
#infoPanel {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  font-size: 1.5rem;
}
h2 {
  font-size: 3rem;
  margin: 20px;
  width: 100%;
}
p {
  text-align: left;
  margin: 10px 20px;
  text-indent: 2rem;
}
a {
  cursor: pointer;
  text-decoration: underline;
  transition: all 0.3s ease;
}
a:hover {
  opacity: 0.5;
}
b {
  font-weight: 600;
}
#rights{
  position: absolute;
  bottom: 0px;
  width: 100%;
  text-align: center;
  display: block;
  align-self: center;
  padding: 2px;
  font-size: 1rem;
  font-family: 'Source Code Pro', monospace;
  font-style: italic;
}
</style>

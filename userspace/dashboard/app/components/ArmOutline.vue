<template>
  <div
    id="armOutline"
    :class="`disable-select ${clickedStop ? 'stopped-outline' : ''}`"
  >
    <img
      id="outlineMask"
      src="/profile_outline.png"
      alt="a thin outline of a robotic arm"
    />
    <div id="outlineTexture"></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'

@Component
export default class armOutline extends Vue {
  @Prop({ type: Boolean, required: true }) readonly clickedStop!: boolean
}
</script>

<style scoped>
#armOutline {
  position: fixed;
  z-index: -1;
  height: 60vh;
  right: 30px;
  bottom: 0px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  animation: 24s linear infinite 1s both spinFade;
}
#armOutline.stopped-outline {
  animation: 6s ease infinite stoppedBlur;
}

#armOutline.stopped-outline #outlineTexture{
  background: red;
  animation: none;
}
#outlineMask {
  position: relative;
  z-index: 10;
  height: 100%;
  opacity: 1;
}
#outlineTexture {
  position: absolute;
  background: conic-gradient(
    from 3.1416rad at 52% 50%,
    white,
    transparent,
    transparent,
    white
  );
  transform-origin: 52% 50%;
  height: 300%;
  width: 600%;
  animation: 24s linear infinite 1s both spinGradient;
  border: 1px solid red;
}
@keyframes spinGradient {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(-720deg);
  }
}

@keyframes spinFade {
  4% {
    opacity: 1;
    filter: blur(0px);
  }
  10% {
    opacity: 0.5;
    filter: blur(5px);
  }
  18% {
    opacity: 1;
    filter: blur(0px);
  }
  30% {
    opacity: 0.5;
    filter: blur(5px);
  }
  36% {
    opacity: 1;
    filte6r: blur(0px);
  }
  50% {
    opacity: 0.5;
    filter: blur(5px);
  }
  65% {
    opacity: 1;
    filter: blur(0px);
  }
  78% {
    opacity: 0.5;
    filter: blur(5px);
  }
  87% {
    opacity: 1;
    filter: blur(0px);
  }
  97% {
    opacity: 0.5;
    filter: blur(5px);
  }
}

@keyframes stoppedBlur {
  0% {
    opacity: .4;
    filter: blur(0px);
  }
  50% {
    opacity: 0.4;
    filter: blur(5px);
  }
  100% {
    opacity: .4;
    filter: blur(0px);
  }
}
</style>

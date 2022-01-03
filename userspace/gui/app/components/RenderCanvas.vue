<template>
  <canvas id="renderCanvas" ref="renderCanvas"></canvas>
</template>

<script lang="ts">
// libs
import { Component, Vue, Prop, Watch } from 'vue-property-decorator'

import * as BABYLON from 'babylonjs'
import * as GUI from 'babylonjs-gui'
import 'babylonjs-loaders'

// import { gsap } from 'gsap'
// components

// types
import { ArmPose } from '@/types/ArmPose'
// miscellaneous
import BabylonController from '@/utils/BabylonController'

@Component
export default class RenderCanvas extends Vue {
  @Prop({ type: Object, required: true }) readonly pose!: ArmPose
  unpluggedPose: ArmPose = {
    joint_1: 0.017956436942507398,
    joint_2: -0.9737956905041772,
    joint_3: -0.7701755099417158,
    joint_4: -0.10276360990249185,
    joint_5: 1.6879406729438893,
    joint_6: -0.04612139081680539,
    module: -1
  }

  openingHand = 0.5
  BC!: BabylonController

  created() {}

  async mounted() {
    const canvas = this.$refs.renderCanvas as HTMLCanvasElement
    this.BC = new BabylonController(canvas)

    this.BC.engine.displayLoadingUI()
    await this.initScene()
    this.updatePose()
    this.BC.engine.hideLoadingUI()

    // this.BC.scene.debugLayer.show()

    this.BC.engine.runRenderLoop(() => {
      this.BC.scene.render()
    })
  }

  async initScene() {
    const scene = this.BC.scene
    scene.createDefaultEnvironment()
    scene.getMeshByName('BackgroundPlane')!.dispose()

    const skybox = scene.getMeshByName('BackgroundSkybox')!
    const backgroundMat = new BABYLON.BackgroundMaterial('customSkybox', scene)
    backgroundMat.reflectionTexture = new BABYLON.CubeTexture(
      'https://raw.githubusercontent.com/Faber-smythe/magic-reflect/master/environment.env',
      scene
    )
    backgroundMat.reflectionTexture.coordinatesMode =
      BABYLON.Texture.SKYBOX_MODE
    backgroundMat.reflectionBlur = 0.15
    skybox.material = backgroundMat

    // This creates and positions the camera
    const camera = new BABYLON.ArcRotateCamera(
      'camera1',
      0,
      0,
      1,
      new BABYLON.Vector3(0, 3, -10),
      scene
    )
    camera.setTarget(new BABYLON.Vector3(0, 0.3, 0))
    camera.alpha = 3

    // Camera parameters
    camera.attachControl(this.BC.canvas, true)
    camera.radius = 1
    camera.wheelPrecision = 50
    camera.panningSensibility = 1000
    camera.minZ = 0.1
    camera.upperBetaLimit = Math.PI * 0.8

    // Creating the light
    const light1 = new BABYLON.HemisphericLight(
      'light1',
      new BABYLON.Vector3(0, 1, 0),
      scene
    )

    // light intensity
    light1.intensity = 1

    await BABYLON.SceneLoader.ImportMeshAsync('', '/', 'xarm-6.glb', scene)
    /**
     * Custom metallic material
     */

    const satinMeshes = scene.meshes.filter(
      (mesh) =>
        (mesh.name.includes('_primitive1') &&
          !mesh.name.includes('Link6_primitive1')) ||
        mesh.name.includes('Link6_primitive0')
    )
    const nodeMaterial = await BABYLON.NodeMaterial.ParseFromSnippetAsync(
      'GPY7R7#9',
      scene
    )
    satinMeshes.forEach((mesh) => {
      mesh.material = nodeMaterial
    })

    // this.displaySlider()

    // apply current pose to the scene
    const link1 = scene.getTransformNodeByName('Link1')
    const link2 = scene.getTransformNodeByName('Link2')
    const link3 = scene.getTransformNodeByName('Link3')
    const link4 = scene.getTransformNodeByName('Link4')
    const link5 = scene.getTransformNodeByName('Link5')
    const head = scene.getTransformNodeByName('Link6')
    scene.registerBeforeRender(() => {
      if (link1) {
        // gsap.to(link1.rotation, {
        //   duration,
        //   x: 0,
        //   y: this.pose.joint_1,
        //   z: 0
        // })
        link1.rotation = new BABYLON.Vector3(0, this.pose.joint_1, 0)
      }

      if (link2) {
        // gsap.to(link2.rotation, {
        //   duration,
        //   x: -this.pose.joint_2 - Math.PI / 2,
        //   y: -Math.PI / 2,
        //   z: Math.PI / 2
        // })
        link2.rotation = new BABYLON.Vector3(
          -this.pose.joint_2 - Math.PI / 2,
          -Math.PI / 2,
          Math.PI / 2
        )
      }
      if (link3) {
        // gsap.to(link3.rotation, {
        //   duration,
        //   x: 0,
        //   y: this.pose.joint_3,
        //   z: 0
        // })
        link3.rotation = new BABYLON.Vector3(0, this.pose.joint_3, 0)
      }
      if (link4) {
        // gsap.to(link4.rotation, {
        //   duration,
        //   x: -this.pose.joint_4 - Math.PI / 2,
        //   y: -Math.PI / 2,
        //   z: Math.PI / 2
        // })
        link4.rotation = new BABYLON.Vector3(
          -this.pose.joint_4 - Math.PI / 2,
          -Math.PI / 2,
          Math.PI / 2
        )
      }
      if (link5) {
        // gsap.to(link5, {
        //   duration,
        //   rotation: this.pose.joint_5 + Math.PI / 2,
        //   y: -Math.PI / 2,
        //   z: -Math.PI / 2
        // })
        // console.log(link5.rotation.x)
        // console.log(link5.rotation)
        link5.rotation = new BABYLON.Vector3(
          this.pose.joint_5 + Math.PI / 2,
          -Math.PI / 2,
          -Math.PI / 2
        )
      }
      if (head) {
        // gsap.to(head.rotation, {
        //   duration,
        //   x: -this.pose.joint_6 - Math.PI / 2,
        //   y: -Math.PI / 2,
        //   z: Math.PI / 2
        // })
        head.rotation = new BABYLON.Vector3(
          -this.pose.joint_6 - Math.PI / 2,
          -Math.PI / 2,
          Math.PI / 2
        )
      }

      scene.animationGroups.forEach((anim) => {
        anim.play()
        anim.goToFrame((this.openingHand / 85) * anim.to)
        anim.pause()
      })
    })
  }

  @Watch('pose')
  updatePose() {
    console.log(this.pose)
    if (this.pose.module >= 0) {
      this.openingHand = this.pose.module
    }
  }

  /**
   * GUI SLIDER FOR INTERACTION
   */
  displaySlider() {
    // initialize the arm's position
    let rotationLink1 = -42
    let rotationLink2 = 54
    let rotationLink3 = 43
    let rotationLink4 = 180
    let rotationLink5 = -42
    let rotationHead = 12
    let openingHand = 58.5

    const advancedTexture =
      GUI.AdvancedDynamicTexture.CreateFullscreenUI('Rotations UI')

    const panel = new GUI.StackPanel()
    panel.width = '220px'
    panel.horizontalAlignment = GUI.Control.HORIZONTAL_ALIGNMENT_RIGHT
    panel.verticalAlignment = GUI.Control.VERTICAL_ALIGNMENT_CENTER
    advancedTexture.addControl(panel)

    const addSlider = (
      title: string,
      initialValue: number,
      onChange: (value: any) => void,
      min: number,
      max: number,
      unit: string
    ) => {
      const label = new GUI.TextBlock()
      label.text = title + ' : ' + (0).toFixed(1) + unit
      label.height = '30px'
      label.color = 'white'
      panel.addControl(label)

      const slider = new GUI.Slider()
      slider.minimum = min
      slider.maximum = max
      slider.value = initialValue
      slider.height = '20px'
      slider.width = '200px'
      slider.onValueChangedObservable.add(function (value) {
        label.text = title + ' : ' + value.toFixed(1) + unit
        onChange(value)
      })
      panel.addControl(slider)
    }

    // create sliders
    addSlider(
      'Link1 rotation',
      rotationLink1,
      (value) => {
        rotationLink1 = value
      },
      -180,
      180,
      '°'
    )
    addSlider(
      'Link2 rotation',
      rotationLink2,
      (value) => {
        rotationLink2 = value
      },
      -180,
      180,
      '°'
    )
    addSlider(
      'Link3 rotation',
      rotationLink3,
      (value) => {
        rotationLink3 = value
      },
      -180,
      180,
      '°'
    )
    addSlider(
      'Link4 rotation',
      rotationLink4,
      (value) => {
        rotationLink4 = value
      },
      -180,
      180,
      '°'
    )
    addSlider(
      'Link5 rotation',
      rotationLink5,
      (value) => {
        rotationLink5 = value
      },
      -180,
      180,
      '°'
    )
    addSlider(
      'Head rotation',
      rotationHead,
      (value) => {
        rotationHead = value
      },
      -180,
      180,
      '°'
    )
    addSlider(
      'Hand opening',
      openingHand,
      (value) => {
        openingHand = value
      },
      0,
      85,
      ' mm'
    )
  }
}
</script>

<style>
#renderCanvas {
  position: fixed;
  /* z-index: 1; */
  left: 0px;
  top: 0px;
  width: 100vw;
  height: 100vh;
}

#inspector-host,
#scene-explorer-host {
  /* position: absolute !important; */
  z-index: 999;
  height: 100%;
  /* overflow-y: scroll; */
}
#inspector-host #actionTabs .tabs {
  /* overflow-y: scroll; */
}
#scene-explorer-host .title,
#inspector-host .title,
#scene-explorer-host .label,
#inspector-host .label {
  font-size: inherit;
  color: inherit;
  font-style: inherit;
  font-weight: inherit;
  margin-bottom: 0px;
}
</style>

<template>
  <canvas id="renderCanvas" ref="renderCanvas"></canvas>
</template>

<script lang="ts">
// libs
import { Component, Vue, Prop, Watch } from 'vue-property-decorator'
import * as BABYLON from 'babylonjs'
import * as GUI from 'babylonjs-gui'
import 'babylonjs-loaders'
// types
import { ArmPose } from '@/types/ArmPose'
import { Equipment } from '@/types/Equipment'
// miscellaneous
import BabylonController from '@/utils/BabylonController'

@Component
export default class RenderCanvas extends Vue {
  @Prop({ type: Object, required: true }) readonly pose!: ArmPose
  @Prop({ type: Boolean, required: true }) readonly watching!: boolean
  @Prop({ type: Boolean, required: true }) readonly clickedStop!: boolean
  @Prop({ type: Object, required: false }) readonly equipped?: Equipment
  unpluggedPose: ArmPose = {
    joint_1: 0.017956436942507398,
    joint_2: -0.9737956905041772,
    joint_3: -0.7701755099417158,
    joint_4: -0.10276360990249185,
    joint_5: 1.6879406729438893,
    joint_6: -0.04612139081680539,
    head: {
      equipment: null
    }
  }

  openingHand = 0.5
  BC!: BabylonController
  hand!: BABYLON.TransformNode

  created() {}

  async mounted() {
    const canvas = this.$refs.renderCanvas as HTMLCanvasElement
    this.BC = new BabylonController(canvas)

    this.BC.engine.displayLoadingUI()
    await this.initScene()
    this.updateEquipment()
    this.BC.engine.hideLoadingUI()

    /** Watch canvas resize event to adjust the 3D scene **/
    const resizeWatcher = new ResizeObserver(() => {
      this.BC.engine.resize()
    })
    resizeWatcher.observe(this.$refs.renderCanvas as HTMLElement)

    // this.BC.scene.debugLayer.show()

    this.BC.engine.runRenderLoop(() => {
      this.BC.scene.render()
    })
  }

  @Watch('clickedStop')
  setCameraControl() {
    if (this.clickedStop) {
      this.BC.camera.detachControl()
    } else {
      this.BC.camera.attachControl(this.BC.canvas)
    }
  }

  @Watch('equipped')
  updateEquipment() {
    const scene = this.BC.scene
    // clear any previous equipment
    this.hand = scene.getTransformNodeByName(
      'hand_base'
    )! as BABYLON.TransformNode
    if (this.hand) this.hand.setEnabled(false)
    if (this.equipped) {
      // enable appropriate equipment
      switch (this.equipped.name.toLowerCase()) {
        case 'hand':
          this.hand.setEnabled(true)
          break
        default:
          break
      }
    }
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
      'GPY7R7#10',
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

    scene.animationGroups.forEach((anim) => {
      console.log(anim)
    })

    scene.registerBeforeRender(() => {
      if (this.watching) {
        if (link1) {
          link1.rotation = new BABYLON.Vector3(0, this.pose.joint_1, 0)
        }

        if (link2) {
          link2.rotation = new BABYLON.Vector3(
            -this.pose.joint_2 - Math.PI / 2,
            -Math.PI / 2,
            Math.PI / 2
          )
        }
        if (link3) {
          link3.rotation = new BABYLON.Vector3(0, this.pose.joint_3, 0)
        }
        if (link4) {
          link4.rotation = new BABYLON.Vector3(
            -this.pose.joint_4 - Math.PI / 2,
            -Math.PI / 2,
            Math.PI / 2
          )
        }
        if (link5) {
          link5.rotation = new BABYLON.Vector3(
            this.pose.joint_5 + Math.PI / 2,
            -Math.PI / 2,
            -Math.PI / 2
          )
        }
        if (head) {
          head.rotation = new BABYLON.Vector3(
            -this.pose.joint_6 - Math.PI / 2,
            -Math.PI / 2,
            Math.PI / 2
          )
        }
      }
      scene.animationGroups.forEach((anim) => {
        anim.play()
        anim.goToFrame((this.openingHand / 85) * anim.to)
        anim.pause()
      })
    })
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
    const openingHand = 58.5

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
        this.openingHand = value
      },
      0,
      85,
      ' mm'
    )
  }
}
</script>

<style>
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

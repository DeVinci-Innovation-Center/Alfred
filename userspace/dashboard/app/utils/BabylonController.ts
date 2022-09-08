import * as BABYLON from 'babylonjs'
import { Scene } from 'babylonjs'
import * as GUI from 'babylonjs-gui'

import { Position2 } from '../types/miscellaneous'

const RAD2DEG = 180 / Math.PI
const DEG2RAD = Math.PI / 180

export default class BabylonController {
  canvas!: HTMLCanvasElement
  engine!: BABYLON.Engine
  scene!: Scene
  GUI!: GUI.AdvancedDynamicTexture
  SM!: BABYLON.SpriteManager
  AM!: BABYLON.AssetsManager
  camera!: BABYLON.ArcRotateCamera
  light!: BABYLON.HemisphericLight

  settings = {
    debugLayer: false,
    fov: 1, // field of view
    brightness: 1
  }

  constructor(canvas: HTMLCanvasElement) {
    // Setting up
    this.canvas = canvas
    this.engine = new BABYLON.Engine(canvas, true)
    this.engine.setHardwareScalingLevel(1 / window.devicePixelRatio)
    this.scene = new BABYLON.Scene(this.engine)

    // set the canvas background to transparent
    this.scene.clearColor = new BABYLON.Color4(0, 0, 0, 0)

    // This creates and positions the camera
    this.camera = new BABYLON.ArcRotateCamera(
      'camera1',
      0,
      0,
      1,
      new BABYLON.Vector3(0, 3, -10),
      this.scene
    )
    this.camera.setTarget(new BABYLON.Vector3(0, 0.3, 0))
    this.camera.alpha = 3

    // Camera parameters
    this.camera.attachControl(this.canvas, true)
    this.camera.radius = 1
    this.camera.wheelPrecision = 50
    this.camera.panningSensibility = 1000
    this.camera.minZ = 0.1
    this.camera.fov = this.settings.fov
    this.camera.upperBetaLimit = Math.PI * 0.8

    // Creating the light
    this.light = new BABYLON.HemisphericLight(
      'light1',
      new BABYLON.Vector3(0, 1, 0),
      this.scene
    )

    // light intensity
    this.light.intensity = this.settings.brightness

    // Initialize Babylon GUI
    this.GUI = GUI.AdvancedDynamicTexture.CreateFullscreenUI(
      'UI',
      true,
      this.scene
    )

    // Toggle debuglayer
    if (this.settings.debugLayer) {
      this.scene.debugLayer.show()
    }
  }

  handleImmersivePicking(
    meshCallback?: Function,
    spriteCallback?: Function,
    outsideCallback?: Function
  ) {
    // Handle clicking events
    this.scene.onPointerDown = (_event, pickResult) => {
      /** CHECK FOR MESHES **/
      if (pickResult && pickResult.pickedMesh) {
        if (meshCallback) {
          meshCallback()
        } else {
          console.log('picked a mesh :', pickResult.pickedMesh.name)
        }
      }
      /** CHECK FOR SPRITES **/
      const search = this.scene.pickSprite(
        this.scene.pointerX,
        this.scene.pointerY
      )
      if (search && search.hit && search.pickedSprite) {
        if (spriteCallback) {
          spriteCallback(search.pickedSprite)
        } else {
          console.log('picked a sprite :', search.pickedSprite.name)
        }
      }
      if (!(search && search.hit) || (pickResult && pickResult.pickedMesh)) {
        if (outsideCallback) outsideCallback()
      }
    }
  }

  worldToScreenCoordinates(coordinates: BABYLON.Vector3): BABYLON.Vector2 {
    const camera = this.scene.cameras[0]
    const projection = BABYLON.Vector3.Project(
      coordinates,
      BABYLON.Matrix.Identity(),
      this.scene.getTransformMatrix(),
      camera.viewport.toGlobal(
        this.canvas.clientWidth,
        this.canvas.clientHeight
      )
    )
    return new BABYLON.Vector2(projection.x, projection.y)
  }

  angleBetweenTwoVectors(vec1: BABYLON.Vector3, vec2: BABYLON.Vector3): number {
    const normalized1 = BABYLON.Vector3.Normalize(vec1)
    const normalized2 = BABYLON.Vector3.Normalize(vec2)

    const dotVec = BABYLON.Vector3.Dot(normalized2, normalized1)

    /** arcCos of dot vector **/
    const angleRadians = Math.acos(dotVec) // radians
    const angleDeegres = this.radiansToDegrees(angleRadians) // deegre

    return angleDeegres
  }

  /**
   * Return 3D cartesian coordinates for the specific hotspots into the displayed spheremap
   * @param {Hotspot} hotspot
   * @param {Number} sphereRadius
   */
  generate3DPosition(hotspotPosition: Position2, sphereRadius: number) {
    /** ------------------------------------------------------------------
     * Generate polar coordinates according to 2D cartesian coordinates of the specific hotspot
     * ------------------------------------------------------------------ */

    const longitude = RAD2DEG * (hotspotPosition.x / sphereRadius)
    const latitude =
      RAD2DEG *
      (2 * Math.atan(Math.exp(hotspotPosition.y / sphereRadius)) - Math.PI / 2)

    /** ------------------------------------------------------------------
     * Generate 3D cartesian coordinates according to polar coordinates (latitude and longitude)
     * ------------------------------------------------------------------ */

    // First send the point from the origin onto the sphere's wall.
    // Then we'll rotate the vector from the origin with two angles
    const origin = new BABYLON.Vector3(0, 0, sphereRadius)

    // Converting to radians and computing the rotation on both planes
    const phi = latitude * DEG2RAD
    const theta = (270 - longitude) * DEG2RAD

    // BABYLON can't rotate a Vector3 with Euler, it needs Quaternion.
    const vecNull = BABYLON.Vector3.Zero() // Quaternion needs a reference to compute
    const quat = BABYLON.Quaternion.FromEulerAngles(phi, theta, 0) // conversion
    const cartesianCoordinates = origin.rotateByQuaternionToRef(quat, vecNull)

    return cartesianCoordinates
  }

  radiansToDegrees(radians: number) {
    return radians * (180 / Math.PI)
  }

  degreesToRadians(degrees: number) {
    return degrees / (180 / Math.PI)
  }
}

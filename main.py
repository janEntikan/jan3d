from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from direct.actor.Actor import Actor


body_keys = [
    'age',

    'torso_belly_fat_upper',
    'torso_shoulder_width',
    'torso_chest_width',
    'torso_breast_size',
    'torso_waist_width',
    'torso_belly_fat_upper',
    'torso_belly_fat_lower',
    'torso_butt_size',
    'torso_butt_roundness',
    'torso_hips_width',

    'legs_upper_fat',
    'legs_lower_fat',
]


face_keys = [
    'eyebrow_length_in',
    'eyebrow_length_out',
    'eyebrow_volume_in',
    'eyebrow_volume_out',

    'face_eye_open',
    'face_ear_height',
    'face_nose_bridge_width',
    'face_nose_bridge_length',
    'face_nose_wings_width',
    'face_nose_tip',
    'face_nose_tip_length',
    'face_nose_height',
    'face_cheekbone',
    'face_cheek',
    'face_lips',
    'face_jaw_width',
    'face_chin_size',
    'face_chin_shape',

    'mouth_l',
    'mouth_a',
    'mouth_o',
    'mouth_m',
    'mouth_pout',
    'mouth_teeth',

    'emotion_smile',
    'emotion_angry',
    'emotion_afraid',
]




class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) 

        render.setShaderAuto()

        self.jan = Actor("jan.bam")
        self.jan.reparent_to(render)
        char = self.jan.find('**/+Character').node()  
        for key in body_keys:
            char.get_bundle(0).freeze_joint(key, 0.5)

        self.jan.loop("walk_forward")


app = MyApp()
app.run()


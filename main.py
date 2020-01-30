from direct.showbase.ShowBase import ShowBase

import simplepbr
from direct.actor.Actor import Actor
from panda3d.core import WindowProperties
from panda3d.core import NodePath
from panda3d.core import TextureStage
from panda3d.core import CharacterSlider
from panda3d.core import DirectionalLight, AmbientLight
from panda3d.core import MouseButton

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) 
        base.win.set_clear_color((0,0,0,0))
        simplepbr.init()

        self.cam_pivot = NodePath("cam pivot")
        self.cam_pivot.reparentTo(render)
        base.cam.reparent_to(self.cam_pivot)
        base.cam.set_pos(0,-2.7,1.8)
        self.cam_pivot.set_h(180)
        self.cam_pivot.set_y(0.2)

        self.jan = Actor("jan.bam")
        self.jan_char = self.jan.find('**/+Character').node()  
        self.jan.play("idle")
        self.jan.reparent_to(render)
        for joint in self.jan.getJoints():
            if type(joint) == CharacterSlider:
                self.set_shapekey(joint.name, 0.0)

        self.set_shapekey("mouth_s", 1)
        self.set_shapekey("face_eye_open", 1)
        self.set_shapekey("emotion_smile", 0.8)
        self.set_shapekey("face_nose_bridge_width", 0.6)
        self.set_shapekey("face_nose_wings_width", 0.6)
        self.set_shapekey("torso_breast_size", 0.6)



        alight = AmbientLight('alight')
        alight.setColor((0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)

        sun = DirectionalLight("sun")
        sun.set_color((1,1,1,1))
        sun_np = render.attachNewNode(sun)
        render.set_light(sun_np)
        sun_np.set_h(180)
        sun_np.set_p(-20)

        self.move_speed = 0.5
        self.zoom_speed = 0.5
        self.last_mouse = [0, 0]

        self.accept("wheel_up", self.zoom_out)
        self.accept("wheel_down", self.zoom_in)
        self.taskMgr.add(self.update)

    def set_shapekey(self, shapekey, value):
        self.jan_char.get_bundle(0).freeze_joint(shapekey, value)

    def zoom_in(self):
        base.cam.set_y(base.cam.get_y()-self.zoom_speed)

    def zoom_out(self):
        base.cam.set_y(base.cam.get_y()+self.zoom_speed)

    def update(self, task):
        if base.mouseWatcherNode.is_button_down(MouseButton.one()):
            new_x = base.mouseWatcherNode.getMouseX()
            new_y = base.mouseWatcherNode.getMouseY()
            x = self.last_mouse[0] - new_x
            y = self.last_mouse[1] - new_y
            self.last_mouse = [new_x, new_y]
            pivot = self.cam_pivot
            pivot.set_z(pivot.get_z()+(y*self.move_speed))
            pivot.set_h(pivot.get_h()+(x*(self.move_speed*640)))
        return task.cont


app = MyApp()
app.run()


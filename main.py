import simplepbr

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import WindowProperties
from panda3d.core import NodePath
from panda3d.core import TextureStage
from panda3d.core import CharacterSlider
from panda3d.core import DirectionalLight, AmbientLight
from panda3d.core import MouseButton
from panda3d.core import TextNode


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
        self.jan.loop("walk_forward")
        self.jan.reparent_to(render)

        self.sliders = {}
        for j, joint in enumerate(self.jan.getJoints()):
            if type(joint) == CharacterSlider:
                self.set_shapekey(joint.name, 0)
                self.sliders[joint.name] = DirectSlider(
                    range=(0,1), value=0, pageSize=0.2, 
                    command=self.set_shapekey_slider, extraArgs=[joint.name]
                )
                y_pos = 4-(j/20)
                slider = self.sliders[joint.name]
                slider.set_scale(0.25)
                slider.set_x(-1.5)
                slider.set_z(y_pos)
                slider_label = OnscreenText(
                    joint.name, pos=(-1.25, y_pos, 0), scale=0.04,
                    fg=(1,1,1,1), align=TextNode.ALeft)

        sun = DirectionalLight("sun")
        sun.set_color((1,0.8,0.8,1))
        sun_np = render.attachNewNode(sun)
        render.set_light(sun_np)
        sun_np.set_h(180)
        sun_np.set_p(-50)

        moon = DirectionalLight("moon")
        moon.set_color((0.8,0.8,1,1))
        moon_np = render.attachNewNode(moon)
        render.set_light(moon_np)
        moon_np.set_p(-50)

        self.move_speed = 0.5
        self.zoom_speed = 0.5
        self.last_mouse = [0, 0]

        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)
        self.taskMgr.add(self.update)

    def set_shapekey_slider(self, shapekey):
        self.set_shapekey(shapekey, self.sliders[shapekey]['value'])

    def set_shapekey(self, shapekey, value):
        self.jan_char.get_bundle(0).freeze_joint(shapekey, value)

    def zoom_out(self):
        new_zoom = base.cam.get_y()-self.zoom_speed
        base.cam.set_y(new_zoom)

    def zoom_in(self):
        new_zoom = base.cam.get_y()+self.zoom_speed
        if new_zoom > -1.2:
            new_zoom = -1.2
        base.cam.set_y(new_zoom)

    def update(self, task):
        if base.mouseWatcherNode.is_button_down(MouseButton.three()):
            new_x = base.mouseWatcherNode.getMouseX()
            new_y = base.mouseWatcherNode.getMouseY()
            x = self.last_mouse[0] - new_x
            y = self.last_mouse[1] - new_y
            self.last_mouse = [new_x, new_y]
            pivot = self.cam_pivot
            pivot.set_z(pivot.get_z()+(y*self.move_speed))
            pivot.set_h(pivot.get_h()+(x*(self.move_speed*640)))
        else:
            self.last_mouse = [0, 0]
        return task.cont


app = MyApp()
app.run()
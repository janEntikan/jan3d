import simplepbr

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import WindowProperties
from panda3d.core import MultitexReducer
from panda3d.core import NodePath
from panda3d.core import TextureStage
from panda3d.core import CharacterSlider
from panda3d.core import DirectionalLight, AmbientLight, PointLight
from panda3d.core import MouseButton
from panda3d.core import TextNode


class CharacterCreator(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) 
        base.win.set_clear_color((0,0,0,0))
        simplepbr.init()
        self.multitex_reducer = MultitexReducer()

        #load textures
        self.textures = {}

        # camera/control
        self.cam_pivot = NodePath("cam pivot")
        self.cam_pivot.reparentTo(render)
        base.cam.reparent_to(self.cam_pivot)
        base.cam.set_pos(0,-2.7,1.8)
        self.cam_pivot.set_h(180)
        self.cam_pivot.set_y(0.2)
        base.camLens.set_near(0.5)
        base.camLens.set_far(64)
        self.move_speed = 0.5
        self.zoom_speed = 0.5
        self.last_mouse = [0, 0]
        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)
        self.taskMgr.add(self.update_camera)

        # sliders
        self.sliders = {}
        self.y_pos = 0.9

        # jan model
        self.jan = Actor(
            {
                "body": "jan/jan.bam",
            },
            {
                "body":{},
            }
        )
        self.jan.play("loop")
        self.make_sliders(self.jan)
        #self.jan.flatten_strong()
        #self.jan.post_flatten()
        #self.multitex_reducer.scan(self.jan)
        #self.multitex_reducer.flatten(base.win)

        self.jan.reparent_to(render)
        self.jan.set_transparency(True)
        self.light_scene()
        render.ls()
        render.analyze()

    def set_shapekey_slider(self, node, shapekey):
        self.set_shapekey(node, shapekey, self.sliders[shapekey]['value'])

    def set_shapekey(self, node, shapekey, value):
        chars = node.find_all_matches('**/+Character')
        for char in chars:
            char.node().get_bundle(0).freeze_joint(shapekey, value)
        
    def zoom_out(self):
        new_zoom = base.cam.get_y()-self.zoom_speed
        base.cam.set_y(new_zoom)

    def zoom_in(self):
        new_zoom = base.cam.get_y()+self.zoom_speed
        if new_zoom > -1.2:
            new_zoom = -1.2
        base.cam.set_y(new_zoom)

    def update_camera(self, task):
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

    def make_sliders(self, node):
        for j, joint in enumerate(node.getJoints()):
            if type(joint) == CharacterSlider:
                if not joint.name in self.sliders:
                    self.set_shapekey(node, joint.name, 0)
                    self.sliders[joint.name] = DirectSlider(
                        range=(0,1), value=0, pageSize=0.2, 
                        command=self.set_shapekey_slider, extraArgs=[node, joint.name]
                    )
                    self.y_pos -= 0.05
                    slider = self.sliders[joint.name]
                    # slider["value"] = 0.5
                    slider.set_scale(0.25)
                    slider.set_x(-1.5)
                    slider.set_z(self.y_pos)
                    slider_label = OnscreenText(
                        joint.name, pos=(-1.25, self.y_pos, 0), scale=0.04,
                        fg=(1,1,1,1), align=TextNode.ALeft)

    def light_scene(self):
        sun = DirectionalLight("sun")
        sun.set_color((1,0.8,0.8,1))
        sun_np = render.attachNewNode(sun)
        render.set_light(sun_np)
        sun_np.set_h(185)
        sun_np.set_p(50)

        moon = DirectionalLight("moon")
        moon.set_color((0.8,0.8,1,1))
        moon_np = sun_np.attachNewNode(moon)
        render.set_light(moon_np)
        moon_np.set_h(180)

app = CharacterCreator()
app.run()

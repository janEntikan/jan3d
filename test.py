from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from direct.actor.Actor import Actor


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) 
        render.setShaderAuto()

        self.jan = Actor("jan.bam")
        self.jan.reparent_to(render)
        #self.jan.ls()

        char = self.jan.find('**/+Character').node()  
        print(char.writeParts(ostream))
        char.get_bundle(0).freeze_joint('torso_breast_size', 1.0)
       

app = MyApp()
app.run()



jan Entikan pana sina e ilo pali jan pi musi jan.
ona li sona pi mani ala.

## Exporting:
* $ blender jan.blend
* clear pose
* "apply single modifier" on body and eyebrows
* save as jan-a.blend
* $ blend2bam jan-a.blend jan.bam --texture=embed
* $ python main.py

## Making clothing:

Currently the only approach I can think of is this:
* Edit body mesh
* Select faces in the general shape of clothing
* Duplicate (shift-d) and Seperate (p)
* select the seperated shape in object mode
* make sure its "base" shapekey is selected
* straighten end edges (sleeves, collars, etc)
* optionally extrude these edges
* use sculpt mode to improve shape (draw, smooth and elastic deform mostly)
This way you inherrit all weights and UV's.
The shapekeys make this approach very volitile and messing
with the vertices a lot can make things collapse easily.
When adding new shapekeys to the body mesh, you would have to reshape each piece of clothing to fit that shapekey. This is terrible and the reason I've not made any clothing yet. Will need some automatic way to transfer shapekeys.
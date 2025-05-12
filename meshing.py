
import gmsh

def rectangle_mesh(mesh_name='beam', elem_size=1., length=100., height=20., display=False):
    """
    Create rectangular 2D structured mesh.
    """

    gmsh.initialize()


    gmsh.model.add(mesh_name)


    geom = gmsh.model.geo

    # Procedure to generate 2D geometry:
    # POINTS -> LINES -> CURVE LOOPS -> FACES (SURFACES)

    # Create points: geom.addPoint(x, y, z)
    p1 = geom.addPoint(0, 0, 0)
    p2 = geom.addPoint(0, height, 0)
    p3 = geom.addPoint(-length, height, 0)
    p4 = geom.addPoint(-length, 0, 0)

    # Create lines between the points:
    l1 = geom.addLine(p1, p2)
    l2 = geom.addLine(p2, p3)
    l3 = geom.addLine(p3, p4)
    l4 = geom.addLine(p4, p1)

    # Before creating a face (surface), create a curve loop
    loop1 = geom.addCurveLoop([l1, l2, l3, l4])

    # Define the surface as a list of curve loops (only one here,
    # representing the external contour, since there are no holes):
    face1 = geom.addPlaneSurface([loop1, ])

    # Create "Physical Groups" in Gmsh ("sets" in Abaqus):
    pg_rig = gmsh.model.addPhysicalGroup(1, [l1,], name="RIGHT")
    pg_top = gmsh.model.addPhysicalGroup(1, [l2,], name="TOP")
    pg_lef = gmsh.model.addPhysicalGroup(1, [l3,], name="LEFT")
    pg_bot = gmsh.model.addPhysicalGroup(1, [l4,], name="BOTTOM")

    pg_all = gmsh.model.addPhysicalGroup(2, [face1,], name="ALL")

    # Define seeds explicitly along lines to produce a structured mesh
    nx = int(length / elem_size) + 1
    ny = int(height / elem_size) + 1
    geom.mesh.setTransfiniteCurve(l1, ny)
    geom.mesh.setTransfiniteCurve(l3, ny)
    geom.mesh.setTransfiniteCurve(l2, nx)
    geom.mesh.setTransfiniteCurve(l4, nx)

    # Transfinite interpolation algorithm in the parametric plane to create a structured grid:
    geom.mesh.setTransfiniteSurface(face1)

    # To create quadrangles instead of triangles, use setRecombine:
    geom.mesh.setRecombine(2, face1)

    # Synchronize before meshing
    geom.synchronize()

    # Create "Physical Groups" node sets for point load and displacement monitor node:
    # Unlike the other PhysicalGroups on these dim=0: Means it's a group of points (nodes in mesh)
    pg_TopRCorner = gmsh.model.addPhysicalGroup(0, [p2,], name="TopRCorner") # Point load 
    pg_BotRCorner = gmsh.model.addPhysicalGroup(0, [p1,], name="BotRCorner") # Node to monitor displacement

    # Export node sets and 2D elements
    gmsh.option.setNumber('Mesh.SaveGroupsOfNodes', 1)  # All physical groups of nodes are saved with their original tags
    gmsh.option.setNumber('Mesh.SaveGroupsOfElements', -100)  # All physical groups of elements are saved with their original tags

    # Generate 2D mesh
    gmsh.model.mesh.generate(2)

    # Export the mesh in Abaqus format (inp extension)
    gmsh.write(mesh_name + ".inp")

    # To visualize the model, open the GUI
    if display:
        gmsh.fltk.run()

    # This should be called when done using the Gmsh Python API
    gmsh.finalize()
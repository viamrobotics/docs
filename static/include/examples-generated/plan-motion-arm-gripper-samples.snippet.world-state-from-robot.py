# Add a table obstacle to a WorldState
table_origin = Pose(x=-202.5, y=-546.5, z=-19.0)
table_dims = Vector3(x=635.0, y=1271.0, z=38.0)
table_object = Geometry(center=table_origin,
                        box=RectangularPrism(dims_mm=table_dims))

obstacles_in_frame = GeometriesInFrame(reference_frame="world",
                                       geometries=[table_object])

# Create a WorldState that has the GeometriesInFrame included
world_state = WorldState(obstacles=[obstacles_in_frame])

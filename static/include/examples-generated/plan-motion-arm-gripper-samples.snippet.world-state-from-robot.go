// Add a table obstacle to a WorldState
obstacles := make([]spatialmath.Geometry, 0)

tableOrigin := spatialmath.NewPose(
	r3.Vector{X: -202.5, Y: -546.5, Z: -19.0},
	&spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
)
tableDims := r3.Vector{X: 635.0, Y: 1271.0, Z: 38.0}
tableObj, err := spatialmath.NewBox(tableOrigin, tableDims, "table")
obstacles = append(obstacles, tableObj)

// Create a WorldState that has the GeometriesInFrame included
obstaclesInFrame := referenceframe.NewGeometriesInFrame(referenceframe.World, obstacles)
worldState, err := referenceframe.NewWorldState([]*referenceframe.GeometriesInFrame{obstaclesInFrame}, nil)
if err != nil {
	logger.Fatal(err)
}

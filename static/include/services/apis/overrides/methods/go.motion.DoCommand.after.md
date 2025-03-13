The built-in motion service makes use of `DoCommand` to allow Go SDK users to request the motion service to generate a plan, or to execute a plan.
The following example shows how to use `DoCommand` to generate a plan and execute it:

```go {class="line-numbers linkable-line-numbers"}

func main() {
    moveReq := motion.MoveReq{ // populate MoveReq however you would like to
        ComponentName: myArm,
        Destination:   destPose,
        Constraints:   motionplan.ConstraintsFromProtobuf(linearConstraintPb),
        WorldState:    worldState,
    }
    approach, err := planMoveReq(moveReq, motionService)
    if err != nil {
        logger.Fatal(err)
    }

    cmd := map[string]interface{}{builtin.DoExecute: approach}
    _, ok := doOverWire(motionService, cmd)[builtin.DoExecute]
    if !ok {
        panic("not ok exec1")
    }
}

func planMoveReq(moveReq motion.MoveReq, ms motion.Service) (motionplan.Trajectory, error) {
    proto, err := moveReq.ToProto(ms.Name().Name)
    if err != nil {
        return nil, err
    }
    bytes, err := protojson.Marshal(proto)
    if err != nil {
        return nil, err
    }
    cmd := map[string]interface{}{builtin.DoPlan: string(bytes)}
    // simulate going over the wire
    resp, ok := doOverWire(ms, cmd)[builtin.DoPlan]
    if !ok {
        return nil, errors.New("not ok plan")
    }

    // the client will need to decode the response still
    var trajectory motionplan.Trajectory
    err = mapstructure.Decode(resp, &trajectory)
    return trajectory, err
}

func doOverWire(ms motion.Service, cmd map[string]interface{}) map[string]interface{} {
    logger := logging.NewLogger("client")
    command, err := protoutils.StructToStructPb(cmd)
    if err != nil {
        logger.Fatal(err)
    }
    resp, err := ms.DoCommand(context.Background(), command.AsMap())
    if err != nil {
        logger.Fatal(err)
    }
    respProto, err := protoutils.StructToStructPb(resp)
    if err != nil {
        logger.Fatal(err)
    }
    return respProto.AsMap()
}

```

motionService, err := motion.FromProvider(machine, "builtin")
if err != nil {
	logger.Fatal(err)
}

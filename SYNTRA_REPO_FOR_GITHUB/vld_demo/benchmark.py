# Python procedural equivalent of VLD logic
engineWarm = True
TPSsteady = True
crankMissing = True
faultCode_17 = True

if engineWarm and TPSsteady and crankMissing and faultCode_17:
    print("[PY] crank.sensor.suspect = TRUE")

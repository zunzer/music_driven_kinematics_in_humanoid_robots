# Choregraphe bezier export in Python.
def denkerpose():
    names = list()
    times = list()
    keys = list()

    names.append("HeadPitch")
    times.append([0, 1.4])
    keys.append([[-0.171306, [3, -0.0333333, 0], [3, 0.466667, 0]], [-0.170838, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("HeadYaw")
    times.append([0, 1.4])
    keys.append([[0.000263987, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.00426377, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LAnklePitch")
    times.append([0, 1.4])
    keys.append([[0.0828792, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.0828792, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LAnkleRoll")
    times.append([0, 1.4])
    keys.append([[-0.100801, [3, -0.0333333, 0], [3, 0.466667, 0]], [-0.100801, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LElbowRoll")
    times.append([0, 1.4])
    keys.append([[-0.424931, [3, -0.0333333, 0], [3, 0.466667, 0]], [-1.37327, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LElbowYaw")
    times.append([0, 1.4])
    keys.append([[-1.2034, [3, -0.0333333, 0], [3, 0.466667, 0]], [-0.270476, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LHand")
    times.append([0, 1.4])
    keys.append([[0.306987, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.6, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LHipPitch")
    times.append([0, 1.4])
    keys.append([[0.126938, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.126938, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LHipRoll")
    times.append([0, 1.4])
    keys.append([[0.112996, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.112996, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LHipYawPitch")
    times.append([0, 1.4])
    keys.append([[-0.174266, [3, -0.0333333, 0], [3, 0.466667, 0]], [-0.174266, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LKneePitch")
    times.append([0, 1.4])
    keys.append([[-0.0910475, [3, -0.0333333, 0], [3, 0.466667, 0]], [-0.0910475, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LShoulderPitch")
    times.append([0, 1.4])
    keys.append([[1.43942, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.941924, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LShoulderRoll")
    times.append([0, 1.4])
    keys.append([[0.22191, [3, -0.0333333, 0], [3, 0.466667, 0]], [-0.314159, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("LWristYaw")
    times.append([0, 1.4])
    keys.append([[0.102275, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.837486, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RAnklePitch")
    times.append([0, 1.4])
    keys.append([[0.0828791, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.0828791, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RAnkleRoll")
    times.append([0, 1.4])
    keys.append([[0.105024, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.105024, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RElbowRoll")
    times.append([0, 1.4])
    keys.append([[0.425181, [3, -0.0333333, 0], [3, 0.466667, 0]], [1.54296, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RElbowYaw")
    times.append([0, 1.4])
    keys.append([[1.19731, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.779236, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RHand")
    times.append([0, 1.4])
    keys.append([[0.3, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.519789, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RHipPitch")
    times.append([0, 1.4])
    keys.append([[0.126938, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.126938, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RHipRoll")
    times.append([0, 1.4])
    keys.append([[-0.11299, [3, -0.0333333, 0], [3, 0.466667, 0]], [-0.11299, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RHipYawPitch")
    times.append([0, 1.4])
    keys.append([[-0.174266, [3, -0.0333333, 0], [3, 0.466667, 0]], [-0.174266, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RKneePitch")
    times.append([0, 1.4])
    keys.append([[-0.0910475, [3, -0.0333333, 0], [3, 0.466667, 0]], [-0.0910475, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RShoulderPitch")
    times.append([0, 1.4])
    keys.append([[1.4373, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.660384, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RShoulderRoll")
    times.append([0, 1.4])
    keys.append([[-0.22181, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.255963, [3, -0.466667, 0], [3, 0, 0]]])

    names.append("RWristYaw")
    times.append([0, 1.4])
    keys.append([[0.100775, [3, -0.0333333, 0], [3, 0.466667, 0]], [0.795528, [3, -0.466667, 0], [3, 0, 0]]])

    return names, times, keys

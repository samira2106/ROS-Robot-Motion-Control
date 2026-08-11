import rospy
import numpy as np
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.msg import FollowJointTrajectoryGoal, JointTolerance

name_list = ["shoulder_pan_joint","shoulder_lift_joint","elbow_joint","wrist_1_joint","wrist_2_joint","wrist_3_joint"]

def JointVec2JointTrajectoryMsg(q, t, qvel = np.zeros(6), qacc = np.zeros(6)):
    
    jointTrajectoryMsg = JointTrajectory()
    points = []#JointTrajectoryPoint()
    
    if qvel.size != q.size:
        qvel = np.zeros(q.shape)
        
    if qacc.size != q.size:
        qacc = np.zeros(q.shape)
        
    if isinstance(t, list):
        for i in range(len(t)):
            point = JointTrajectoryPoint()
            point.positions = list(q[i])
            point.velocities = list(qvel[i])
            point.accelerations = list(qacc[i])
            point.time_from_start=rospy.Duration(t[i])
            points.append(point)
    else:
        point = JointTrajectoryPoint()
        point.positions = list(q)
        point.velocities = list(qvel)
        point.accelerations = list(qacc)
        point.time_from_start=rospy.Duration(t)
        points.append(point)
        
    jointTrajectoryMsg.joint_names = name_list
    #jointTrajectoryMsg.points = [point] #.points.append(point)
    jointTrajectoryMsg.points = points #.append(point)
    
    return jointTrajectoryMsg

def JointStateMsg2JointState( robot, jointMsg ):
    # Maybe not to be used
    
    return [ jointState, jointVel ]

def  JointVec2FollowJointTrajectoryMsg(q, t, qvel = np.zeros(6), qacc = np.zeros(6)):
    # followJointTrajectoryMsg
    if qvel.size != q.size:
        qvel = np.zeros(q.shape)

    if qacc.size != q.size:
        qacc = np.zeros(q.shape)

    qtol=-1
    qveltol=-1
    qacctol=-1

    followJointTrajectoryMsg = FollowJointTrajectoryGoal()
    followJointTrajectoryMsg.trajectory = JointVec2JointTrajectoryMsg(q,t,qvel,qacc)
    goal_tolerances = []
    path_tolerances = []
    for j in range(q.shape[1]):
        goal_tolerance = JointTolerance()
        path_tolerance = JointTolerance()

        goal_tolerance.name=name_list[j]
        path_tolerance.name=name_list[j]
        goal_tolerance.position=qtol
        goal_tolerance.velocity=qveltol
        goal_tolerance.acceleration=qacctol
        path_tolerance.position=qtol
        path_tolerance.velocity=qveltol
        path_tolerance.acceleration=qacctol
        
        goal_tolerances.append(goal_tolerance)
        path_tolerances.append(path_tolerance)
        
    followJointTrajectoryMsg.goal_tolerance = goal_tolerances
    followJointTrajectoryMsg.path_tolerance = path_tolerances
    followJointTrajectoryMsg.goal_time_tolerance=rospy.Duration(0)
    #followJointTrajectoryMsg.goal_time_tolerance.nsec=int(1e7)  # 10 ms
    return followJointTrajectoryMsg

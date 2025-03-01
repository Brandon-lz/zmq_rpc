from utils.opc_lib import (
    MyOpcClient,
    MyNode,
)

from config import config

period_client = MyOpcClient(
    url=f"opc.tcp://{config['plc']['host']}",
    # url=f"opc.tcp://{config['plc-ip']}:{config['opcua-port']}",
    client_name="period_client",
)
period_client.connect()


# period_client.register_opcvar(
#     [
#         "0:Objects",
#         "2:DeviceSet",
#         "3:PLC_Line1",
#         "3:DataBlocksGlobal",
#         "3:DB702_TCP_Server",
#         "3:HeartBeat",
#     ],
#     name="heart_beat",
# )

# 0:Root,0:Objects,2:MyObject,2:MyVariable

period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["node-heartbeat"]["node_id"],
    ),
    name="heartbeat",
)

print(period_client["heartbeat"].get_value())

period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["node-start"]["node_id"],
    ),
    name="start",
)

period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["node-stop"]["node_id"],
    ),
    name="stop",
)


period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["node-jog-add"]["node_id"],
    ),
    name="jog_add",
)


period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["node-jog-sub"]["node_id"],
    ),
    name="jog_sub",
)


period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["torque-value"]["node_id"],
    ),
    name="torque_value",
)


period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["aim-torque"]["node_id"],
    ),
    name="aim_torque",
)

period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["max-torque"]["node_id"],
    ),
    name="max_torque",
)

period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["output-torque"]["node_id"],
    ),
    name="output_torque",
)

period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["handle-mode"]["node_id"],
    ),
    name="handle_mode",
)

period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["act-torque"]["node_id"],
    ),
    name="act_torque",
)

period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["torque-measure-value"]["node_id"],
    ),
    name="torque_measure_value",
)

period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["torque-measure-value"]["node_id"],
    ),
    name="torque_measure_value",
)

# global_vars.torque_set
period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["torque-current-set-value"]["node_id"],
    ),
    name="torque_current_set_value",
)

# global_vars.torque_set_output
period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["torque-set-output"]["node_id"],
    ),
    name="torque_set_output",
)

# global_vars.torque_feedback
period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["torque-feedback"]["node_id"],
    ),
    name="torque_feedback",
)

# global_vars.torque_finished
period_client.register_opcvar(
    MyNode(
        period_client.get_root_node().server,
        nodeid=config["nodes"]["torque-finished"]["node_id"],
    ),
    name="torque_finished",
)


print(period_client.opc_vars_names)

print("PLC READY")

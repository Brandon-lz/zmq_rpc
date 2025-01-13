from utils.opc_lib import (
    MyOpcClient,
    MyNode,
)

from typing import List, Dict


SEARCH_LIST = ["gswd", "hswd", "ljll", "ssll", "ssrl"]


class BaseNode:
    def __init__(self, opcua_client: MyOpcClient, node: MyNode):
        self.opcua_client = opcua_client
        self.base_node: MyNode = node
        self.base_node_name: str = self.base_node.get_browse_name().Name
        self.children: List[MyNode] = []
        for child in self.base_node.get_children():
            if child.get_browse_name().Name in SEARCH_LIST:
                self.children.append(child)
        self.children_names: List[str] = [
            child.get_browse_name().Name for child in self.children
        ]

    def get_children_values(self) -> tuple[List[str], list]:
        values = self.opcua_client.read_vars(self.children)
        return self.children_names, values


class OpcuaUtil:
    base_nodes: Dict[str, BaseNode] = {}

    def __init__(self, opcua_client: MyOpcClient):
        self.opcua_client = opcua_client

    def add_base_node(self, node_name: str, node: MyNode):
        self.base_nodes[node_name] = BaseNode(self.opcua_client, node)

    def get_base_node(self, node_name: str) -> BaseNode:
        return self.base_nodes.get(node_name)

    def get_values(self):
        res = {}
        for base_node_name, base_node in self.base_nodes.items():
            children_names, values = base_node.get_children_values()
            for name, value in zip(children_names, values):
                res[f"{base_node_name}.{name}"] = value
        return res


opcua_client = MyOpcClient(
    url=f"opc.tcp://159.75.120.46:15555",
    client_name="opcua_client",
)

opcua_client.connect()
print("连接成功")


opcuatuil = OpcuaUtil(opcua_client)


opcuatuil.add_base_node(
    "IFC",
    opcua_client.get_node("ns=2;s=opc.opcua.IFC.IFC"),  # 从客户端中拷贝出来的父节点
)

opcuatuil.add_base_node(
    "LXWC",
    opcua_client.get_node("ns=2;s=opc.opcua.LXWC.LXWC"),  # 从客户端中拷贝出来的父节点
)

opcuatuil.add_base_node(
    "WTS",
    opcua_client.get_node("ns=2;s=opc.opcua.WTS.WTS"),  # 从客户端中拷贝出来的父节点
)


opcuatuil.get_values()

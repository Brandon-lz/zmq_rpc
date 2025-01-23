"""
 * @Author: wl.liuzhao 
 * @Date: 2023-03-29 11:33:20 
 * @Last Modified by:   wl.liuzhao 
 * @Last Modified time: 2023-03-29 11:33:20 
 - 自改Node，方便数据操作
"""

from opcua.common.node import Node
from opcua import ua
from typing import List


class MyNode(Node):
    """新增一些简单的功能

    Args:
        Node (_type_): _description_
    """

    name = None
    description = "plc Node variable"
    _alive: int = 3
    varianttype = ua.VariantType
    # _keep_alive:bool=True

    def get_value(self):
        try:
            return super().get_value()
        finally:
            self._alive = 3

    def set_value(self, value, varianttype=None):
        try:
            return super().set_value(value, varianttype)
        finally:
            self._alive = 3

    def set_word(self, value: int):
        value = ua.DataValue(ua.Variant(value, ua.VariantType.UInt16))
        self.set_value(value)

    def set_int(self, value: int):
        value = ua.DataValue(ua.Variant(value, ua.VariantType.Int16))
        self.set_value(value)

    def set_real(self, value: float):
        value = ua.DataValue(ua.Variant(value, ua.VariantType.Float))
        self.set_value(value)

    def set_bool(self, value: bool):
        value = ua.DataValue(ua.Variant(value, ua.VariantType.Boolean))
        self.set_value(value)

    def get_referenced_nodes(
        self,
        refs=ua.ObjectIds.References,
        direction=ua.BrowseDirection.Both,
        nodeclassmask=ua.NodeClass.Unspecified,
        includesubtypes=True,
    ):
        """
        returns referenced nodes based on specific filter
        Paramters are the same as for get_references

        """
        references = self.get_references(
            refs, direction, nodeclassmask, includesubtypes
        )
        nodes = []
        for desc in references:
            node = MyNode(self.server, desc.NodeId)
            nodes.append(node)
        return nodes

    def get_children(
        self,
        refs=ua.ObjectIds.HierarchicalReferences,
        nodeclassmask=ua.NodeClass.Unspecified,
    ) -> List["MyNode"]:
        return self.get_referenced_nodes(
            refs, ua.BrowseDirection.Forward, nodeclassmask
        )

    def get_child(self, path):
        """
        get a child specified by its path from this node.
        A path might be:
        * a string representing a qualified name.
        * a qualified name
        * a list of string
        * a list of qualified names
        """
        if type(path) not in (list, tuple):
            path = [path]
        rpath = self._make_relative_path(path)
        bpath = ua.BrowsePath()
        bpath.StartingNode = self.nodeid
        bpath.RelativePath = rpath
        result = self.server.translate_browsepaths_to_nodeids([bpath])
        result = result[0]
        result.StatusCode.check()
        # FIXME: seems this method may return several nodes
        return MyNode(self.server, result.Targets[0].TargetId)

    def get_node_children_path(self):
        paths = []
        for i in self.get_children():
            paths.append(i.get_path(as_string=True)[1:])
        return paths

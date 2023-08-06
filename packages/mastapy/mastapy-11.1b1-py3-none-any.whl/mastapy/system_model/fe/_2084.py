'''_2084.py

ElementFaceGroupWithSelection
'''


from mastapy.system_model.fe import _2086
from mastapy.nodal_analysis.component_mode_synthesis import _197
from mastapy.fe_tools.vis_tools_global import _1159
from mastapy._internal.python_net import python_net_import

_ELEMENT_FACE_GROUP_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.FE', 'ElementFaceGroupWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementFaceGroupWithSelection',)


class ElementFaceGroupWithSelection(_2086.FEEntityGroupWithSelection['_197.CMSElementFaceGroup', '_1159.ElementFace']):
    '''ElementFaceGroupWithSelection

    This is a mastapy class.
    '''

    TYPE = _ELEMENT_FACE_GROUP_WITH_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElementFaceGroupWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

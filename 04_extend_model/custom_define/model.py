"""A local Define-XML v2.1 model extended with a vendor attribute.

Adds vnd:ReviewStatus to ItemDef while inheriting everything else from the
stock model. Hand this package to a loader to round-trip extended documents:

    loader = LD.ODMLoader(DL.XMLDefineLoader(model_package="custom_define",
                                             local_model=True))
"""
from odmlib.define_2_1.model import *          # bring in the full stock model
import odmlib.define_2_1.model as DEF
import odmlib.ns_registry as NS
import odmlib.typed as T

NS.NamespaceRegistry(prefix="vnd", uri="https://example.org/vnd/v1.0")


class ItemDef(DEF.ItemDef, merge_fields=True):
    ReviewStatus = T.String(namespace="vnd")

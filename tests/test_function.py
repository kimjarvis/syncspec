import sys
import json
from pathlib import Path
import networkx as nx

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from syncspec.function import syncspec

#
# def test_syncspec():
#     graph, meta = syncspec(
#         path="../syncspec-test/input/",
#         output="../syncspec-test/output/",
#         import_path="../syncspec-test/input/",
#         keyvalue={},
#         log_file="syncspec.log"
#     )
#
#     nx.nx_pydot.write_dot(graph, "syncspec.dot")
#     with open("syncspec.json", "w", encoding='utf-8') as f:
#         json.dump(meta, f)
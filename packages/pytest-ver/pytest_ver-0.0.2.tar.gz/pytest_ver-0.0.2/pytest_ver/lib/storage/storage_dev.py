import json
import os

from .storage import Storage
from .. import services


# -------------------
class StorageDev(Storage):
    # -------------------
    def __init__(self):
        self._protocol_path = os.path.join(services.cfg.outdir, 'protocol.json')
        self._trace_path = os.path.join(services.cfg.outdir, 'trace.json')
        self._summary_path = os.path.join(services.cfg.outdir, 'summary.json')

    # -------------------
    def save_protocol(self, protocols):
        # TODO save file with unique name
        with open(self._protocol_path, 'w', encoding='utf=8') as fp:
            json.dump(protocols, fp, ensure_ascii=True, indent=2)

    # -------------------
    def get_protocols(self):
        # TODO read all protocol files
        protocols = None
        with open(self._protocol_path, 'r', encoding='utf=8') as fp:
            protocols = json.load(fp)
        return protocols

    # -------------------
    def save_trace(self, trace):
        # TODO save file with unique name
        with open(self._trace_path, 'w', encoding='utf=8') as fp:
            json.dump(trace, fp, ensure_ascii=True, indent=2)

    # -------------------
    def get_trace(self):
        # TODO read all trace files
        trace = None
        with open(self._trace_path, 'r', encoding='utf=8') as fp:
            trace = json.load(fp)
        return trace

    # -------------------
    def save_summary(self, summary):
        # TODO save file with unique name
        with open(self._summary_path, 'w', encoding='utf=8') as fp:
            json.dump(summary, fp, ensure_ascii=True, indent=2)
        pass

    # -------------------
    def get_summary(self):
        trace = None
        with open(self._summary_path, 'r', encoding='utf=8') as fp:
            trace = json.load(fp)
        return trace

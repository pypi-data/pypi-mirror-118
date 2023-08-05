from . import services
from .cfg import Cfg
from .protocol import Protocol
from .report.report import Report
from .storage.storage import Storage
from .summary import Summary
from .trace_matrix import TraceMatrix
from .verifier import Verifier


# -------------------
class PytestHarness:
    # -------------------
    def __init__(self):
        services.cfg = Cfg()
        services.cfg.report()

        services.storage = Storage.factory()
        services.summary = Summary()
        services.trace = TraceMatrix()
        services.proto = Protocol()
        self.proto = services.proto
        self.ver = Verifier()

    # -------------------
    def report(self):
        rep = Report()
        rep.report()

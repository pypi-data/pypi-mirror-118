from . import services
from .cfg import Cfg
from .log.logger import Logger
from .log.logger_stdout import LoggerStdout
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
        services.logger = LoggerStdout()
        services.logger.init()

        services.cfg = Cfg()
        services.cfg.init()

        # after cfg indicates where log files are stored
        # can use normal logger
        services.logger = Logger()
        services.logger.init()

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

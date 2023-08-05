import inspect
import os

from . import services
from .result_summary import ResultSummary


# -------------------
class Verifier:
    def __init__(self):
        pass

    # -------------------
    def verify(self, actual, reqid=None):
        loc = self._format_location(inspect.stack()[1])

        rs = ResultSummary()
        rs.actual = actual
        rs.expected = True
        rs.reqid = reqid
        rs.location = loc

        if actual:
            self._save_result_pass(rs)
            return

        if reqid is not None:
            self._save_result_fail(rs)

    # -------------------
    def _save_result_pass(self, rs):
        rs.passed()
        services.proto.add_result(rs)

    # -------------------
    def _save_result_fail(self, rs):
        rs.failed()
        services.proto.add_result(rs)

    # -------------------
    def _format_location(self, stack):
        fname = os.path.basename(stack.filename)
        return f'{fname}({stack.lineno})'

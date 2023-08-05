import datetime

from . import services


# -------------------
class Protocol:
    # -------------------
    def __init__(self):
        self._protocols = []
        self._protocol = None
        self._step = None

    # -------------------
    def protocol(self, proto_id: str, desc):
        self._protocol = {
            'proto_id': proto_id.upper(),
            'desc': desc,
            'steps': [],
        }
        self._protocols.append(self._protocol)
        self._step = None
        self.save()

    # -------------------
    def step(self, desc):
        now = datetime.datetime.now(datetime.timezone.utc)
        dts = now.strftime('%Y%m%d %H:%M:%S')
        self._step = {
            'desc': desc,
            'dts': dts,
            'results': [],
        }
        self._protocol['steps'].append(self._step)
        self.save()

    # -------------------
    def add_result(self, rs):
        # TODO add location, and srsid
        # TODO write to results file
        services.logger.dbg(f'{rs.result}: reqid:{rs.reqid} actual:{rs.actual} expected:{rs.expected}')
        self._step['results'].append(rs)
        if rs.reqid is not None:
            services.trace.add_proto(rs.reqid, self._protocol['proto_id'], rs.location)
        services.summary.add_result(rs.reqid, self._protocol['proto_id'], rs.result)
        self.save()

    # -------------------
    def save(self):
        services.storage.save_protocol(self._protocols)

# -------------------
class PageInfo:
    # -------------------
    class Header:
        left = 'TBD'
        middle = '<b>TBD</b>'
        right = 'TBD'

    # -------------------
    class Footer:
        left = 'TBD'
        middle = 'TBD'
        right = 'TBD'

    # -------------------
    def __init__(self):
        # TODO add defaults from cfg.json, then allow overrides per document
        self.header = PageInfo.Header()
        self.header.left = 'TBD'
        self.header.middle = '<b>TBD</b>'
        self.header.right = 'TBD'

        self.footer = PageInfo.Footer()
        self.footer.left = 'foot_left'
        self.footer.middle = '(c)2021 This document is private and confidential.'
        self.footer.right = '<pageno>'

    # -------------------
    def __getitem__(self, item):
        if item == 'header':
            return self.header

        if item == 'footer':
            return self.footer

        print(f'ERR bad item name: {item}')
        # TODO abort

    # -------------------
    def set_tp_cfg(self):
        # TODO add page orientation? page size?
        self.header.left = 'DCO: TPC-002'
        self.header.middle = '<b>Test Results</b>'
        self.header.right = 'Rev. A'

    # -------------------
    def set_trace_cfg(self):
        # TODO add page orientation? page size?
        self.header.left = 'DCO: TM-003'
        self.header.middle = '<b>Trace Matrix - Automated Results</b>'
        self.header.right = 'Rev. B'

    # -------------------
    def set_summary_cfg(self):
        # TODO add page orientation? page size?
        self.header.left = ''
        self.header.middle = '<b>Automated Test Summary</b>'
        self.header.right = ''

    # -------------------
    def report(self, fp):
        fp.write(f"{'Header left': <20}: {self.header.left}\n")
        fp.write(f"{'Header middle': <20}: {self.header.middle}\n")
        fp.write(f"{'Header right': <20}: {self.header.right}\n")

        fp.write(f"{'Footer left': <20}: {self.footer.left}\n")
        fp.write(f"{'Footer middle': <20}: {self.footer.middle}\n")
        fp.write(f"{'Footer right': <20}: {self.footer.right}\n")

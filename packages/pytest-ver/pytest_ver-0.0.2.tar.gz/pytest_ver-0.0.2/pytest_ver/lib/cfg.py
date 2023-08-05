from .page_info import PageInfo


# -------------------
class Cfg:
    # -------------------
    def __init__(self):
        self.outdir = 'out'
        self.storage_type = 'dev'
        # one of formal, dryrun, dev
        self.test_run_type = 'dev'
        self.test_run_id = 'dev-001'
        self.dts_format = "%Y-%m-%d %H:%M:%S %Z"
        self.page_info = PageInfo()

        # TODO add header/footer to cfg.json

    # -------------------
    def report(self):
        print('Cfg:')
        print(f"  {'Output Dir': <20}: {self.outdir}")
        print(f"  {'Storage Type': <20}: {self.storage_type}")
        print(f"  {'Test Run Id': <20}: {self.test_run_id}")
        print('')

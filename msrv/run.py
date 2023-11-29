from msrv.settings.configs import ASCM

apx = (
    ASCM()
    .enable(oauth2=True, cors=True, overload_watch=False, rate_limits=True)
    .mount(all_routes=True)
    .build()
)

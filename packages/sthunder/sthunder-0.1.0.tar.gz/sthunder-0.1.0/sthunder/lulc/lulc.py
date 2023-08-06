import os
from wlts import WLTS


SERVICE_URL = "https://brazildatacube.dpi.inpe.br/wlts/"
SERVICE_TOKEN = os.environ.get('BDC_TOKEN')
UNDEF = 'No-Data'

service = WLTS(url=SERVICE_URL, access_token=SERVICE_TOKEN)
tjs = service.tj(latitude=[-12.], longitude=[-47.],
                 collections='mapbiomas5_amazonia,mapbiomas5_cerrado,'
                             'mapbiomas5_caatinga,mapbiomas5_mata_atlantica,'
                             'mapbiomas5_pampa,mapbiomas5_pantanal',
                 start_date='2010')

for tj in tjs['trajectories']:
    print(tj.trajectory)
    tjcs = list(filter(lambda row: UNDEF not in row['class'], tj.trajectory))
    if len(tjcs) == 0:
        tjcs = [UNDEF]

    print(tjcs[-1])
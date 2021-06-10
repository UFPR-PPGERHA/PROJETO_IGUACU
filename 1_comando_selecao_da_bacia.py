import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point

#   Este codigo irá ler o arquivo tipo shapefile da bacia do iguaçu, e irá ver quais estaçõs da relação
# nacional estão na bacia do iguaçu e por fim irá criar Coords_Bruto.txt com a relação de todas as estações
# da bacia do iguaçu.

f_shps = '/home/seb/Projeto-iguacu/Contorno/Bacia_do_iguacu.shp'
f_coords = '/home/seb/Projeto-iguacu/relacao_estacoes_HidroWeb.txt'

#Cria um geodataframe com o a base de dados nacional.
dt_coords = pd.read_csv(f_coords, '\t')
dt_coords['Coordinates'] = list(zip(dt_coords.Longitude, dt_coords.Latitude))
dt_coords['Coordinates'] = dt_coords['Coordinates'].apply(Point)
dt_coords = gpd.GeoDataFrame(dt_coords, geometry='Coordinates')

#Cria um poligono geometrico com o shapefile do contorno da bacia do iguaçu.
dt_shps = gpd.read_file(f_shps)
geom = dt_shps.iloc[0, :]
geom = geom['geometry'].buffer(0)

#Faz a interseção entre o geodataframe e o poligono da bacia, resultando na lista de estações da bacia do iguaçu.
dt_coords['Dentro'] = dt_coords['Coordinates'].intersects(geom)
dt_coords = dt_coords[dt_coords['Dentro']]
dt_coords = dt_coords[['Codigo', 'Latitude', 'Longitude']]

#Salva a lista das estações da bacia do Iguaçu no arquivo Coords_Bruto.txt.
dt_coords.to_csv('Coords_Bruto.txt', sep='\t', index=False)

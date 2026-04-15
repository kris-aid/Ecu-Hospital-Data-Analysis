def generate_cords(geo_pd):
    """
    Genera una lista de coordenadas (latitud, longitud) a partir de un DataFrame de GeoPandas.

    Parámetros:
    geo_pd (GeoDataFrame): Un DataFrame de GeoPandas que contiene geometrías.

    Retorna:
    list: Una lista de tuplas, donde cada tupla contiene (latitud, longitud).
    """
    cords = []
    for geom in geo_pd.geometry:
        if geom.geom_type == 'Point':
            cords.append((geom.y, geom.x))
        elif geom.geom_type in ['LineString', 'Polygon']:
            for coord in geom.coords:
                cords.append((coord[1], coord[0]))
        elif geom.geom_type in ['MultiPoint', 'MultiLineString', 'MultiPolygon', 'GeometryCollection']:
            for part in geom.geoms:
                if part.geom_type == 'Point':
                    cords.append((part.y, part.x))
                    print("Point detected")
                else:
                    for coord in part.coords:
                        cords.append((coord[1], coord[0]))
    return cords

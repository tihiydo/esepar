import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup} from 'react-leaflet';

import 'leaflet/dist/leaflet.css';
import './PointsOfInvincibility.css';
import L from 'leaflet';
import icon from '../images/marker-icon.png';
import iconShadow from '../images/marker-shadow.png';

const PointsOfInvincibility = () => 
{
  
  let DefaultIcon = L.icon({
      iconUrl: icon,
      shadowUrl: iconShadow
  });

  L.Marker.prototype.options.icon = DefaultIcon;

  useEffect(() => {
    document.getElementsByClassName("leaflet-control-zoom")[0].remove();
  });

  return (
  <MapContainer center={[49.0139, 31.2858]} zoom={6.4}>

      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://st1.deepstatemap.live/styles/DSUkraineUk/{z}/{x}/{y}@2x.png"
      /> 

      <Marker position={[48.237689, 28.273496]}>
        <Popup>
          Поставити цю хуйню, не так то просто я 6 часов фіксив те що не сходяться версії
        </Popup>
      </Marker>
      
    </MapContainer>
  );
}

//GeoJSON - use for Ukraine borders
//https://api.maptiler.com/maps/ch-swisstopo-lbm-dark/{z}/{x}/{y}.png?key=nSfkrzMVniyKN2CUi3FV
//0.0001500 коф зміщення приблизний, але не точний, методом тика (коф різниця від гугл карт)

export default PointsOfInvincibility;
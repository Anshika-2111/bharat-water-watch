let map;
let markerLayer = [];

const riskColors = {
  Safe:   { color: '#00e676', icon: '🟢' },
  Medium: { color: '#ffb300', icon: '🟡' },
  High:   { color: '#ff3d3d', icon: '🔴' },
};

function initMap(districts) {
  map = L.map('map', { center: [22.5, 80.0], zoom: 5 });
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '© OpenStreetMap © CARTO',
    subdomains: 'abcd', maxZoom: 19
  }).addTo(map);
  updateMapMarkers(districts);
}

function updateMapMarkers(districts) {
  markerLayer.forEach(m => map.removeLayer(m));
  markerLayer = [];

  districts.forEach(d => {
    const { color, icon } = riskColors[d.risk_level] || riskColors['Safe'];
    const marker = L.circleMarker([d.latitude, d.longitude], {
      radius: 14, fillColor: color,
      color: '#000', weight: 1.5,
      opacity: 1, fillOpacity: 0.85,
    });
    marker.bindPopup(`
      <div style="font-family:'DM Sans',sans-serif;min-width:180px;">
        <div style="font-weight:700;font-size:1rem;margin-bottom:4px;">${icon} ${d.name}</div>
        <div style="color:#aaa;font-size:0.8rem;margin-bottom:8px;">${d.state}</div>
        <div style="display:flex;gap:8px;margin-bottom:6px;">
          <div style="background:rgba(255,255,255,0.08);border-radius:8px;padding:6px 10px;text-align:center;flex:1">
            <div style="font-weight:700">${d.ph_level}</div>
            <div style="font-size:0.7rem;color:#aaa;">pH</div>
          </div>
          <div style="background:rgba(255,255,255,0.08);border-radius:8px;padding:6px 10px;text-align:center;flex:1">
            <div style="font-weight:700">${d.tds_level}</div>
            <div style="font-size:0.7rem;color:#aaa;">TDS</div>
          </div>
        </div>
        <div style="background:${color}22;border:1px solid ${color}55;border-radius:6px;padding:4px 10px;text-align:center;color:${color};font-size:0.78rem;font-weight:600;text-transform:uppercase;">
          ${d.risk_level} Risk
        </div>
      </div>
    `);
    marker.addTo(map);
    markerLayer.push(marker);
  });
}
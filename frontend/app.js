const API = 'https://bharat-water-watch-api.onrender.com/api';
let allDistricts = [];

async function loadDistricts() {
  try {
    const res = await fetch(`${API}/districts/`);
    allDistricts = await res.json();
    renderStats(allDistricts);
    renderCards(allDistricts);
    if (typeof initMap === 'function') initMap(allDistricts);
  } catch (err) {
    document.getElementById('cardsGrid').innerHTML =
      '<p style="color:var(--high);grid-column:1/-1;padding:2rem">⚠️ Could not connect to backend. Make sure Flask is running on port 5000.</p>';
  }
}

function renderStats(data) {
  document.getElementById('totalDistricts').textContent = data.length;
  document.getElementById('highRisk').textContent  = data.filter(d => d.risk_level === 'High').length;
  document.getElementById('safeZones').textContent = data.filter(d => d.risk_level === 'Safe').length;
  document.getElementById('mediumRisk').textContent= data.filter(d => d.risk_level === 'Medium').length;
}

function renderCards(data) {
  const grid = document.getElementById('cardsGrid');
  if (!grid) return;
  if (!data.length) {
    grid.innerHTML = '<p style="color:var(--text-muted);grid-column:1/-1;padding:2rem;text-align:center">No districts found.</p>';
    return;
  }
  grid.innerHTML = data.map((d, i) => `
    <div class="district-card risk-${d.risk_level}" style="animation-delay:${i * 0.05}s">
      <div class="card-header">
        <div>
          <div class="card-name">${d.name}</div>
          <div class="card-state">${d.state}</div>
        </div>
        <span class="risk-badge badge-${d.risk_level}">${d.risk_level}</span>
      </div>
      <div class="card-metrics">
        <div class="metric">
          <div class="metric-val">${d.ph_level ?? '—'}</div>
          <div class="metric-key">pH Level</div>
        </div>
        <div class="metric">
          <div class="metric-val">${d.tds_level ?? '—'}</div>
          <div class="metric-key">TDS (ppm)</div>
        </div>
      </div>
      <div class="card-updated">🕐 Updated: ${new Date(d.last_updated).toLocaleDateString('en-IN', {day:'numeric',month:'short',year:'numeric'})}</div>
    </div>
  `).join('');
}

function filterCards() {
  const q = document.getElementById('searchBox').value.toLowerCase();
  const filtered = allDistricts.filter(d =>
    d.name.toLowerCase().includes(q) || d.state.toLowerCase().includes(q)
  );
  renderCards(filtered);
}

function filterMap(level, btn) {
  document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  const filtered = level === 'all' ? allDistricts : allDistricts.filter(d => d.risk_level === level);
  if (typeof updateMapMarkers === 'function') updateMapMarkers(filtered);
}

document.addEventListener('DOMContentLoaded', loadDistricts);
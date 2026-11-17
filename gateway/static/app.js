const state = {
  visualEvents: [],
  run: null,
  map: null,
  mapRunId: null,
  mapLoading: false,
  ai: null,
  aiLoading: false,
  mode: "single",
  modeTouched: false,
  singleLoading: false,
  singleSeries: null,
};

async function request(path, options = {}) {
  const response = await fetch(path, { headers: { "Content-Type": "application/json" }, ...options });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "璇锋眰澶辫触");
  return data;
}

function text(id, value) { document.getElementById(id).textContent = value ?? "--"; }

function number(value, digits = 1) {
  return value === undefined || value === null || Number.isNaN(Number(value)) ? "--" : Number(value).toFixed(digits);
}

function setPill(id, label, kind = "") {
  const element = document.getElementById(id);
  element.textContent = label;
  element.className = `status-pill ${kind}`;
}

function setActive(role, active) {
  const element = document.querySelector(`[data-role="${role}"]`);
  if (!element) return;
  element.classList.toggle("active", Boolean(active));
  element.setAttribute("aria-pressed", active ? "true" : "false");
}

function setNodeVisibility(ia1Online, st1Online) {
  const ia1Control = document.getElementById("ia1ControlPanel");
  const st1Control = document.getElementById("st1ControlPanel");
  const ia1Hero = document.getElementById("ia1Hero");
  const st1Hero = document.getElementById("st1Hero");
  for (const [element, online] of [
    [ia1Hero, ia1Online],
    [ia1Control, ia1Online],
    [st1Hero, st1Online],
    [st1Control, st1Online],
  ]) {
    if (element) element.classList.toggle("is-offline", !online);
  }
  for (const [panel, online] of [[ia1Control, ia1Online], [st1Control, st1Online]]) {
    if (panel) panel.querySelectorAll("button").forEach(button => { button.disabled = !online; });
  }
}

function clearOfflineNode(ia1Online, st1Online) {
  if (!ia1Online) {
    for (const id of ["temperature", "humidity", "lux", "ia1Time", "ia1Mode", "fanState", "lightState", "shipmentState"]) {
      text(id, "--");
    }
    setPill("ia1State", "鏈繛鎺?, "");
    for (const role of ["auto", "fan-on", "fan-off", "light-on", "light-off"]) setActive(role, false);
    const hint = document.getElementById("ia1ModeHint");
    if (hint) hint.textContent = "IA1 鏈繛鎺ワ紝闈㈡澘淇濇寔绌猴紱鎺ュ洖鑺傜偣鍚庤嚜鍔ㄦ仮澶嶃€?;
  }
  if (!st1Online) {
    for (const id of ["gpsStatus", "latitude", "longitude", "speed", "st1Time", "zoneState", "buzzerState", "transportState"]) {
      text(id, "--");
    }
    setPill("st1State", "鏈繛鎺?, "");
  }
}

function render(data) {
  const ia1 = data.latest.ia1 || {};
  const st1 = data.latest.st1 || {};
  const nodes = data.nodes || {};
  const ia1Online = nodes.ia1 ? Boolean(nodes.ia1.online) : Boolean(ia1.received_at);
  const st1Online = nodes.st1 ? Boolean(nodes.st1.online) : Boolean(st1.received_at);
  setNodeVisibility(ia1Online, st1Online);
  text("temperature", number(ia1.temperature, 1));
  text("humidity", number(ia1.humidity, 1));
  text("lux", number(ia1.lux, 1));
  text("ia1Time", ia1.received_at || "--");
  text("ia1Mode", ia1.mode === "manual" ? "鎵嬪姩" : ia1.mode === "auto" ? "鑷姩" : "--");
  text("fanState", ia1.fan ? "杩愯涓? : "鍏抽棴");
  text("lightState", ia1.light ? "寮€鍚? : "鍏抽棴");
  text("shipmentState", ia1.environment_status === "normal" ? "鍏佽鍑鸿揣" : ia1.environment_status ? "闇€鍏虫敞" : "--");
  const manual = ia1.mode === "manual";
  setActive("auto", ia1.mode === "auto");
  setActive("fan-on", manual && Number(ia1.fan) === 1);
  setActive("fan-off", manual && Number(ia1.fan) === 0);
  setActive("light-on", manual && Number(ia1.light) === 1);
  setActive("light-off", manual && Number(ia1.light) === 0);
  const hint = document.getElementById("ia1ModeHint");
  if (hint) {
    hint.textContent = manual
      ? "褰撳墠鏄墜鍔ㄦā寮忥細椋庢墖/琛ュ厜鍙寜鎸夐挳鎵ц锛屼笉浼氭牴鎹俯婀垮害/鍏夌収鑷姩璋冭妭銆?
      : ia1.mode === "auto"
        ? "褰撳墠鏄嚜鍔ㄦā寮忥細鍏夌収浣庝簬闃堝€间細鑷姩寮€琛ュ厜锛屾俯婀垮害瓒呴檺浼氳嚜鍔ㄥ紑椋庢墖銆?
        : "";
  }
  setPill("ia1State", ia1.environment_status === "normal" ? "鐜姝ｅ父" : ia1.environment_status ? `鐜${ia1.environment_status}` : "绛夊緟鏁版嵁", ia1.environment_status === "normal" ? "good" : ia1.environment_status ? "warn" : "");

  text("gpsStatus", st1.gps_valid ? "GPS宸插畾浣? : "鎼滄槦涓?);
  text("latitude", number(st1.latitude, 6));
  text("longitude", number(st1.longitude, 6));
  text("speed", number(st1.speed, 1));
  text("st1Time", st1.received_at || "--");
  const zoneText = {
    out_of_zone: "宸茶秺鐣?,
    in_zone: "鍖哄煙鍐?,
    in_transit: "杩愯緭涓?,
    gps_searching: "鎼滄槦涓?,
    delivered: "宸查€佽揪",
  }[st1.zone_status] || "--";
  text("zoneState", zoneText);
  text("buzzerState", st1.buzzer ? "鎶ヨ" : "鍏抽棴");
  text("transportState", st1.transport_status === "in_transit" ? "杩愯緭涓? : st1.transport_status === "ready" ? "寰呭懡" : "--");
  setPill("st1State", st1.alarm ? "杩愯緭鎶ヨ" : st1.gps_valid ? "瀹氫綅姝ｅ父" : "鎼滄槦涓?, st1.alarm ? "bad" : st1.gps_valid ? "good" : "warn");

  const mode = document.getElementById("modeBadge");
  mode.textContent = data.demo ? "婕旂ず妯℃嫙妯″紡" : data.broker_connected ? "MQTT宸茶繛鎺? : "绛夊緟MQTT";
  mode.className = `badge ${data.demo || data.broker_connected ? "" : "muted"}`;
  text("lastRefresh", new Date().toLocaleTimeString());
  renderRun(data.run || null, Boolean(st1Online && st1.gps_valid));
  renderEvents(data.events || []);
  clearOfflineNode(ia1Online, st1Online);
}

function setRunPill(label, kind = "") {
  const element = document.getElementById("runState");
  if (!element) return;
  element.textContent = label;
  element.className = `status-pill ${kind}`;
}

function renderRun(run, gpsReady = false) {
  state.run = run;
  const start = document.getElementById("startRun");
  const stop = document.getElementById("stopRun");
  if (!start || !stop) return;
  if (!run) {
    start.disabled = !gpsReady;
    stop.disabled = true;
    setRunPill("鏈紑濮?);
    text("runPoints", "0 鐐?);
    text("runHint", gpsReady
      ? "GPS 宸插畾浣嶏紝鍙互寮€濮嬭矾绾匡紱寮€濮嬭矾绾夸細鍚屾椂寮€濮嬭繍杈撱€?
      : "鍏堢瓑 GPS 瀹氫綅锛屽啀寮€濮嬭矾绾匡紱寮€濮嬭矾绾夸細鍚屾椂寮€濮嬭繍杈撱€?);
    if (!state.map) drawMapPlaceholder("瀹屾垚涓€鍦堝悗鐢熸垚娓╁害鍦板浘");
    return;
  }
  const active = run.status === "active";
  start.disabled = active || !gpsReady;
  stop.disabled = !active;
  setRunPill(active ? "閲囬泦涓? : run.status === "completed" ? "宸插畬鎴? : "宸蹭腑姝?, active ? "warn" : run.status === "completed" ? "good" : "");
  text("runPoints", `${run.points || 0} 鐐?/ 鏈夋晥 ${run.valid_points || 0}`);
  text("runHint", active
    ? `绗?${run.id} 鍦堥噰闆嗕腑锛氬皬杞︽部璺嚎绉诲姩锛岀粨鏉熷悗鐢熸垚娓╁害鍦板浘銆俙
    : run.status === "completed"
      ? `绗?${run.id} 鍦堝凡瀹屾垚锛屽湴鍥惧熀浜?${run.valid_points || 0} 涓湁鏁堢偣銆俙
      : `绗?${run.id} 鍦堝凡涓銆俙);
  if (active && !state.map) {
    drawMapPlaceholder("閲囬泦涓紝缁撴潫鍚庣敓鎴愭俯搴﹀湴鍥?);
  }
  if (run.status === "aborted") {
    state.map = null;
    state.mapRunId = run.id;
    drawMapPlaceholder("鏈湀宸蹭腑姝紝娌℃湁娓╁害鍦板浘");
  }
  if (run.status === "completed" && state.mapRunId !== run.id && !state.mapLoading) {
    loadMap(run.id);
  }
}

async function loadMap(runId) {
  state.mapLoading = true;
  try {
    const data = await request(`/api/map?run_id=${encodeURIComponent(runId)}&metric=temperature&cols=60&rows=60`);
    state.map = data;
    state.mapRunId = runId;
    drawMap(data);
  } catch (error) {
    state.mapRunId = runId;
    state.visualEvents.unshift({ node: "map", level: "alarm", message: error.message, time: new Date().toLocaleTimeString() });
    renderEvents([]);
    drawMapPlaceholder("鍦板浘鐢熸垚澶辫触锛屽埛鏂伴〉闈㈤噸璇?);
  } finally {
    state.mapLoading = false;
  }
}

function drawMapPlaceholder(label) {
  const canvas = document.getElementById("mapCanvas");
  const empty = document.getElementById("mapEmpty");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = "#e1ebe5";
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const x = 32 + (canvas.width - 64) * i / 4;
    const y = 32 + (canvas.height - 64) * i / 4;
    ctx.beginPath(); ctx.moveTo(x, 32); ctx.lineTo(x, canvas.height - 32); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(32, y); ctx.lineTo(canvas.width - 32, y); ctx.stroke();
  }
  ctx.fillStyle = "#64736b";
  ctx.font = "14px Segoe UI";
  ctx.fillText("娓╁害鍦板浘", 32, 24);
  if (empty) {
    empty.style.display = "block";
    empty.textContent = label;
  }
  const stats = document.getElementById("mapStats");
  if (stats) stats.innerHTML = "";
}

function mapColor(value, min, max) {
  if (value === null || value === undefined) return "rgba(0,0,0,0)";
  const t = max === min ? 0.5 : Math.max(0, Math.min(1, (value - min) / (max - min)));
  const hue = 220 - 220 * t;
  return `hsla(${hue}, 72%, 48%, .58)`;
}

function drawMap(data) {
  const canvas = document.getElementById("mapCanvas");
  const empty = document.getElementById("mapEmpty");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const route = data.route || [];
  const points = data.points || [];
  if (!data.enough) {
    ctx.strokeStyle = "#e1ebe5";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const x = 32 + (canvas.width - 64) * i / 4;
      const y = 32 + (canvas.height - 64) * i / 4;
      ctx.beginPath(); ctx.moveTo(x, 32); ctx.lineTo(x, canvas.height - 32); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(32, y); ctx.lineTo(canvas.width - 32, y); ctx.stroke();
    }
  }
  const bounds = data.bounds;
  if (!bounds) {
    if (empty) { empty.style.display = "block"; empty.textContent = "鏈湀娌℃湁鏈夋晥娓╁害鐐?; }
    return;
  }
  const pad = 32;
  const width = canvas.width - pad * 2;
  const height = canvas.height - pad * 2;
  const minLat = bounds.min_lat, maxLat = bounds.max_lat;
  const minLon = bounds.min_lon, maxLon = bounds.max_lon;
  const spanLat = maxLat - minLat || 1e-6;
  const spanLon = maxLon - minLon || 1e-6;
  const cosLat = Math.cos((minLat + maxLat) / 2 * Math.PI / 180);
  const spanX = spanLon * cosLat;
  const scale = Math.min(width / Math.max(spanX, 1e-9), height / Math.max(spanLat, 1e-9));
  const originX = pad + (width - spanX * scale) / 2;
  const originY = canvas.height - pad - (height - spanLat * scale) / 2;
  const toXY = (lat, lon) => [
    originX + (lon - minLon) * cosLat * scale,
    originY - (lat - minLat) * scale,
  ];

  if (data.enough && data.values && data.values.length) {
    const rows = data.values.length;
    const cols = data.values[0].length;
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const value = data.values[row][col];
        if (value === null || value === undefined) continue;
        const lon0 = minLon + spanLon * col / cols;
        const lon1 = minLon + spanLon * (col + 1) / cols;
        const lat0 = minLat + spanLat * row / rows;
        const lat1 = minLat + spanLat * (row + 1) / rows;
        const [x0, y0] = toXY(lat0, lon0);
        const [x1, y1] = toXY(lat1, lon1);
        ctx.fillStyle = mapColor(value, data.min, data.max);
        ctx.fillRect(Math.min(x0, x1), Math.min(y0, y1), Math.abs(x1 - x0) + 0.5, Math.abs(y1 - y0) + 0.5);
      }
    }
  }

  if (route.length) {
    ctx.strokeStyle = "#1d6f92";
    ctx.lineWidth = 3;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.beginPath();
    route.forEach(([lat, lon], index) => {
      const [x, y] = toXY(lat, lon);
      if (index === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke();
  }
  points.forEach(point => {
    const [x, y] = toXY(point.lat, point.lon);
    ctx.fillStyle = point.quality === "ok" ? "#145c3d" : "#b43e3e";
    ctx.beginPath();
    ctx.arc(x, y, 3.5, 0, Math.PI * 2);
    ctx.fill();
  });

  if (empty) empty.style.display = "none";
  const stats = document.getElementById("mapStats");
  if (stats) {
    stats.innerHTML = `
      <span>鏈夋晥鐐?<strong>${points.length}</strong></span>
      <span>鏈€浣?<strong>${number(data.min, 1)} ${data.unit}</strong></span>
      <span>鏈€楂?<strong>${number(data.max, 1)} ${data.unit}</strong></span>
      <span>骞冲潎 <strong>${number(data.avg, 1)} ${data.unit}</strong></span>
      <span>璺嚎鐐?<strong>${route.length}</strong></span>
    `;
  }
}

function renderEvents(events) {
  const container = document.getElementById("events");
  const visible = state.visualEvents.length ? state.visualEvents : events;
  if (!visible.length) { container.innerHTML = '<div class="empty-overlay" style="position:static;padding-top:80px">鏆傛棤鎶ヨ鍜屼簨浠?/div>'; return; }
  container.innerHTML = visible.map(event => `<div class="event ${event.level || ""}"><div class="event-head"><span>${event.node || "system"}</span><span>${event.time || "--"}</span></div><div class="event-message">${escapeHtml(event.message || "浜嬩欢")}</div></div>`).join("");
}

function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char])); }

function aiNumber(value, digits = 1) {
  return value === undefined || value === null || Number.isNaN(Number(value)) ? "--" : Number(value).toFixed(digits);
}

function setForecastCard(metric, item, forecast) {
  const temp = metric === "temperature";
  const prefix = temp ? "aiTemp" : "aiHumidity";
  text(`${prefix}Predicted`, aiNumber(item?.predicted));
  text(`${prefix}Current`, aiNumber(item?.current));
  text(`${prefix}Range`, item?.lower !== null && item?.lower !== undefined
    ? `${aiNumber(item.lower)} 鈥?${aiNumber(item.upper)}`
    : "--");
  const confidence = Number(item?.confidence || 0);
  text(`${prefix}Confidence`, item?.available ? `缃俊搴?${Math.round(confidence * 100)}%` : "缃俊搴?--");
  const card = document.querySelector(`.forecast-card.${temp ? "temp" : "humidity"}`);
  if (card) {
    const label = card.querySelector(".forecast-label");
    if (label) label.innerHTML = `${temp ? "娓╁害" : "婀垮害"} 路 鏈潵 <span class="horizon">${forecast?.horizon_min || 10}</span> 鍒嗛挓`;
    const bar = card.querySelector(".confidence i");
    if (bar) bar.style.width = `${Math.round(confidence * 100)}%`;
  }
}

function renderAI(data) {
  const forecast = data?.forecast || {};
  const temp = forecast.temperature || {};
  const humidity = forecast.humidity || {};
  const available = Boolean(forecast.available);
  const model = forecast.model || {};
  const badge = document.getElementById("aiModel");
  if (badge) {
    badge.textContent = available
      ? `${forecast.source === "route_points" ? "鍘嗗彶璺嚎" : "瀹炴椂鍩虹嚎"} 路 ${forecast.samples || 0} 鏍锋湰`
      : "鏁版嵁涓嶈冻";
    badge.className = `badge ${available ? "" : "muted"}`;
  }
  const summary = document.getElementById("aiSummary");
  if (summary) {
    if (available) {
      summary.textContent = `鍩轰簬 ${forecast.source === "route_points" ? `${forecast.runs || 1} 鍦堣矾绾跨偣` : "鏈€杩?IA1 瀹炴椂鏁版嵁"} 鐨勮秼鍔块娴嬶紝妯″瀷 ${model.name || "SARIMAX"}锛涙暟鍊艰秺浣庣疆淇″害瓒婃湁闄愩€俙;
    } else {
      summary.textContent = forecast.message || "瀹屾垚璺嚎鎴栫瓑寰?IA1 瀹炴椂鏁版嵁鍚庡紑濮嬪垎鏋愩€?;
    }
  }
  setForecastCard("temperature", temp, forecast);
  setForecastCard("humidity", humidity, forecast);
  text("aiMessage", forecast.message || "");
  const updated = document.getElementById("aiUpdated");
  if (updated) updated.textContent = forecast.generated_at ? `鏇存柊 ${new Date(forecast.generated_at).toLocaleTimeString()}` : "--";

  const alerts = data?.alerts || [];
  const container = document.getElementById("aiAlerts");
  const count = document.getElementById("aiAlertCount");
  if (count) count.textContent = `${alerts.length} 鏉;
  if (!container) return;
  if (!alerts.length) {
    container.innerHTML = '<div class="empty-overlay" style="position:static;padding-top:80px">鏆傛棤棰勮锛岀幆澧冩甯?/div>';
    return;
  }
  const labels = { watch: "鍏虫敞", warning: "璀﹀憡", critical: "涓ラ噸" };
  const metricLabels = { temperature: "娓╁害", humidity: "婀垮害", lux: "鍏夌収" };
  container.innerHTML = alerts.map(alert => {
    const level = alert.level || "watch";
    const ack = alert.acknowledged
      ? '<span class="hint">宸茬‘璁?/span>'
      : `<button data-ack="${alert.id}">纭</button>`;
    return `<div class="alert-item ${level}">
      <div class="alert-head">
        <span class="alert-title"><span class="alert-level ${level}">${labels[level] || level}</span> ${metricLabels[alert.metric] || alert.metric}</span>
        <span class="alert-time">${alert.time ? new Date(alert.time).toLocaleTimeString() : "--"}</span>
      </div>
      <div class="alert-message">${escapeHtml(alert.message || "")}</div>
      <div class="alert-foot"><span>${escapeHtml(alert.action || "寤鸿浜哄伐妫€鏌?)}${alert.source === "prediction" ? " 路 棰勬祴瑙﹀彂" : ""}</span>${ack}</div>
    </div>`;
  }).join("");
}

async function loadAI() {
  if (state.aiLoading) return state.ai;
  state.aiLoading = true;
  try {
    const scope = state.mode === "single" ? "?scope=single" : "";
    const data = await request(`/api/ai${scope}`);
    state.ai = data;
    renderAI(data);
    return data;
  } catch (error) {
    const summary = document.getElementById("aiSummary");
    if (summary) summary.textContent = `AI 鏈嶅姟鏆備笉鍙敤锛?{error.message}`;
    return null;
  } finally {
    state.aiLoading = false;
  }
}

async function acknowledgeAlert(id) {
  try {
    await request(`/api/alerts/${id}/ack`, { method: "POST", body: "{}" });
    await loadAI();
  } catch (error) {
    state.visualEvents.unshift({ node: "ai", level: "alarm", message: error.message, time: new Date().toLocaleTimeString() });
    renderEvents([]);
  }
}

function setMode(mode) {
  state.mode = mode === "region" ? "region" : "single";
  document.querySelectorAll(".mode-button").forEach(button => {
    button.classList.toggle("active", button.dataset.mode === state.mode);
  });
  const single = state.mode === "single";
  document.getElementById("singleView").classList.toggle("hidden-view", !single);
  document.getElementById("regionView").classList.toggle("hidden-view", single);
  const hint = document.getElementById("modeHint");
  if (hint) {
    hint.textContent = single
      ? "鍗曠偣妯″紡锛氬皬杞︿笉鍔紝瑙傚療鍚屼竴浣嶇疆鐨勬俯婀垮害/鍏夌収闅忔椂闂村彉鍖栵紝铏氱嚎涓烘湭鏉?10 鍒嗛挓 AI 棰勬祴銆?
      : "鍖哄煙鍦板浘妯″紡锛氱偣鍑烩€滃紑濮嬭矾绾库€濊灏忚溅璺戣捣鏉ワ紝缁撴潫鍚庣敓鎴愬尯鍩熺儹鍔涘浘銆?;
  }
  if (single) {
    loadSingle();
  } else {
    loadAI();
    if (state.run && state.run.status === "completed" && state.mapRunId !== state.run.id) {
      loadMap(state.run.id);
    }
  }
}

function seriesValue(points, key) {
  const values = points.map(point => Number(point[key])).filter(value => Number.isFinite(value));
  return values.length ? values[values.length - 1] : null;
}

function drawSeriesChart(canvasId, metric, series, ai) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#fbfdfb";
  ctx.fillRect(0, 0, width, height);

  const points = (series?.points || []).filter(point => Number.isFinite(Number(point[metric])));
  const forecast = ai?.forecast || {};
  const path = forecast[metric]?.path || [];
  const forecastPath = path.filter(point => Number.isFinite(Number(point.value)));
  if (!points.length && !forecastPath.length) {
    ctx.fillStyle = "#6b7871";
    ctx.font = "14px 'Segoe UI'";
    ctx.fillText("鏆傛棤鏁版嵁锛岀瓑寰?IA1 涓婃姤", 24, height / 2);
    return;
  }

  const pad = { left: 48, right: 18, top: 16, bottom: 28 };
  const plotW = width - pad.left - pad.right;
  const plotH = height - pad.top - pad.bottom;
  const allValues = [
    ...points.map(point => Number(point[metric])),
    ...forecastPath.map(point => Number(point.value)),
  ];
  let minValue = Math.min(...allValues);
  let maxValue = Math.max(...allValues);
  if (minValue === maxValue) {
    minValue -= 1;
    maxValue += 1;
  }
  const padding = (maxValue - minValue) * 0.15;
  minValue -= padding;
  maxValue += padding;
  const allTimes = [
    ...points.map(point => Number(point.ts_ms)),
    ...forecastPath.map(point => Number(point.ts_ms)),
  ];
  const minTime = Math.min(...allTimes);
  const maxTime = Math.max(...allTimes);
  const xOf = ts => pad.left + (Number(ts) - minTime) / Math.max(1, maxTime - minTime) * plotW;
  const yOf = value => pad.top + (maxValue - Number(value)) / (maxValue - minValue) * plotH;

  ctx.strokeStyle = "#e1ebe5";
  ctx.fillStyle = "#7b8881";
  ctx.font = "11px 'Segoe UI'";
  ctx.lineWidth = 1;
  for (let index = 0; index <= 4; index++) {
    const value = minValue + (maxValue - minValue) * index / 4;
    const y = yOf(value);
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(width - pad.right, y);
    ctx.stroke();
    ctx.fillText(value.toFixed(metric === "lux" ? 0 : 1), 4, y + 4);
  }
  const fmtTime = ts => new Date(ts).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  ctx.fillText(fmtTime(minTime), pad.left, height - 8);
  const endText = fmtTime(maxTime);
  ctx.fillText(endText, width - pad.right - ctx.measureText(endText).width, height - 8);

  // 棰勬祴缃俊甯?  if (forecastPath.length > 1) {
    ctx.beginPath();
    forecastPath.forEach((point, index) => {
      const x = xOf(point.ts_ms);
      const y = yOf(point.upper);
      if (index === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    [...forecastPath].reverse().forEach(point => {
      ctx.lineTo(xOf(point.ts_ms), yOf(point.lower));
    });
    ctx.closePath();
    ctx.fillStyle = "rgba(29,111,146,.10)";
    ctx.fill();
  }

  if (points.length > 1) {
    ctx.beginPath();
    points.forEach((point, index) => {
      const x = xOf(point.ts_ms);
      const y = yOf(point[metric]);
      if (index === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.strokeStyle = metric === "temperature" ? "#b96b22" : metric === "humidity" ? "#1d6f92" : "#178451";
    ctx.lineWidth = 2.2;
    ctx.stroke();
  }

  if (forecastPath.length > 1) {
    ctx.beginPath();
    forecastPath.forEach((point, index) => {
      const x = xOf(point.ts_ms);
      const y = yOf(point.value);
      if (index === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.setLineDash([6, 5]);
    ctx.strokeStyle = metric === "temperature" ? "#d18a45" : metric === "humidity" ? "#4c93b2" : "#42a06f";
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.setLineDash([]);
  }
}

function renderSingle(series, ai) {
  const points = series?.points || [];
  const latest = points[points.length - 1] || {};
  const forecast = ai?.forecast || {};
  text("singleTempNow", latest.temperature !== undefined ? `${number(latest.temperature, 1)} 掳C` : "-- 掳C");
  text("singleHumidityNow", latest.humidity !== undefined ? `${number(latest.humidity, 1)} %` : "-- %");
  text("singleLuxNow", latest.lux !== undefined ? `${number(latest.lux, 0)} lx` : "-- lx");
  const badge = document.getElementById("singleStatus");
  if (badge) {
    badge.textContent = points.length ? "鍗曠偣閲囬泦涓? : "绛夊緟 IA1 鏁版嵁";
    badge.className = `badge ${points.length ? "" : "muted"}`;
  }
  const updated = document.getElementById("singleUpdated");
  if (updated) updated.textContent = `鏇存柊 ${new Date().toLocaleTimeString()}`;
  const hint = document.getElementById("singleHint");
  if (hint) {
    hint.textContent = points.length
      ? `鏈€杩?${series.minutes || 30} 鍒嗛挓鍏?${points.length} 涓噰鏍风偣锛?{forecast.message || "AI 棰勬祴鍑嗗涓?}`
      : "璇风‘璁?IA1 宸蹭笂鐢靛苟杩炴帴 MQTT锛岀瓑寰呮暟鎹啓鍏ャ€?;
  }
  drawSeriesChart("tempChart", "temperature", series, ai);
  drawSeriesChart("humidityChart", "humidity", series, ai);
  drawSeriesChart("luxChart", "lux", series, ai);
}

async function loadSingle() {
  if (state.singleLoading) return;
  state.singleLoading = true;
  try {
    const [series, ai] = await Promise.all([
      request("/api/series?node=ia1&minutes=30&limit=1200"),
      loadAI(),
    ]);
    state.singleSeries = series;
    renderSingle(series, ai || state.ai);
  } catch (error) {
    const hint = document.getElementById("singleHint");
    if (hint) hint.textContent = `鍗曠偣鏁版嵁鍔犺浇澶辫触锛?{error.message}`;
  } finally {
    state.singleLoading = false;
  }
}

function setIa1Mode(mode) {
  text("ia1Mode", mode === "auto" ? "鑷姩" : mode === "manual" ? "鎵嬪姩" : "--");
  const hint = document.getElementById("ia1ModeHint");
  if (hint) {
    hint.textContent = mode === "manual"
      ? "褰撳墠鏄墜鍔ㄦā寮忥細椋庢墖/琛ュ厜鍙寜鎸夐挳鎵ц锛屼笉浼氭牴鎹俯婀垮害/鍏夌収鑷姩璋冭妭銆?
      : mode === "auto"
        ? "褰撳墠鏄嚜鍔ㄦā寮忥細鍏夌収浣庝簬闃堝€间細鑷姩寮€琛ュ厜锛屾俯婀垮害瓒呴檺浼氳嚜鍔ㄥ紑椋庢墖銆?
        : "";
  }
}

function reflectCommand(command) {
  if (command.node !== "ia1") return;
  const payload = command.payload || {};
  if (payload.action === "set_mode") {
    setIa1Mode(payload.mode);
    setActive("auto", payload.mode === "auto");
    if (payload.mode === "auto") {
      setActive("fan-on", false);
      setActive("fan-off", false);
      setActive("light-on", false);
      setActive("light-off", false);
    }
  } else if (payload.action === "fan") {
    setIa1Mode("manual");
    setActive("auto", false);
    setActive("fan-on", Number(payload.value) === 1);
    setActive("fan-off", Number(payload.value) === 0);
  } else if (payload.action === "light") {
    setIa1Mode("manual");
    setActive("auto", false);
    setActive("light-on", Number(payload.value) === 1);
    setActive("light-off", Number(payload.value) === 0);
  }
}

async function sendCommand(command) {
  try {
    const result = await request("/api/command", { method: "POST", body: JSON.stringify(command) });
    if (!result.published && !result.demo_applied) throw new Error("鍛戒护鏈彂閫侊細MQTT 鏈繛鎺?);
    reflectCommand(command);
  } catch (error) {
    state.visualEvents.unshift({ node: "web", level: "alarm", message: error.message, time: new Date().toLocaleTimeString() });
    renderEvents([]);
  }
}

async function startRoute() {
  if (state.run && state.run.status === "active") return;
  try {
    const now = new Date();
    const result = await request("/api/run/start", {
      method: "POST",
      body: JSON.stringify({
        label: `${now.toLocaleDateString()} ${now.toLocaleTimeString()}`,
        route_name: "榛樿璺嚎",
        start_transport: true,
      }),
    });
    state.run = result.run;
    state.map = null;
    state.mapRunId = null;
    drawMapPlaceholder("閲囬泦涓紝缁撴潫鍚庣敓鎴愭俯搴﹀湴鍥?);
    await refresh();
  } catch (error) {
    state.visualEvents.unshift({ node: "route", level: "alarm", message: error.message, time: new Date().toLocaleTimeString() });
    renderEvents([]);
  }
}

async function stopRoute() {
  if (!state.run || state.run.status !== "active") return;
  try {
    await request("/api/run/stop", {
      method: "POST",
      body: JSON.stringify({ run_id: state.run.id, status: "completed", end_transport: true }),
    });
    state.map = null;
    state.mapRunId = null;
    await refresh();
  } catch (error) {
    state.visualEvents.unshift({ node: "route", level: "alarm", message: error.message, time: new Date().toLocaleTimeString() });
    renderEvents([]);
  }
}

async function refresh() {
  try { render(await request("/api/state")); } catch (error) { document.getElementById("modeBadge").textContent = "鏈嶅姟鏈繛鎺?; }
}

document.querySelectorAll("[data-command]").forEach(button => button.addEventListener("click", () => sendCommand(JSON.parse(button.dataset.command))));
document.getElementById("startRun").addEventListener("click", startRoute);
document.getElementById("stopRun").addEventListener("click", stopRoute);
document.getElementById("clearVisualEvents").addEventListener("click", () => { state.visualEvents = []; renderEvents([]); });
document.querySelectorAll(".mode-button").forEach(button => {
  button.addEventListener("click", () => {
    state.modeTouched = true;
    setMode(button.dataset.mode);
  });
});
document.getElementById("refreshSingle").addEventListener("click", loadSingle);
document.getElementById("refreshAI").addEventListener("click", () => {
  if (state.mode === "single") loadSingle(); else loadAI();
});
document.getElementById("aiAlerts").addEventListener("click", event => {
  const button = event.target.closest("[data-ack]");
  if (button) acknowledgeAlert(button.dataset.ack);
});
refresh();
setMode("single");
setInterval(refresh, 500);
setInterval(() => { if (state.mode === "single") loadSingle(); else loadAI(); }, 5000);



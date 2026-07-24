# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Visualize: HTML+Canvas visualization via built-in HTTP
# Generates interactive visualizations served through Zap's built-in
# web server. Zap is both backend (physics computation) and frontend
# (HTML/Canvas rendering served via http_server).
# ═══════════════════════════════════════════════════════════════════

# ── HTML Page Generator ──
# Generates a complete HTML page with Canvas for visualization

fn html_page(title, body_content, extra_js)
  let html = "<!DOCTYPE html>"
  html = html + "<html><head><title>" + title + "</title>"
  html = html + "<meta charset='utf-8'>"
  html = html + "<style>"
  html = html + "body { margin: 0; padding: 20px; font-family: monospace; background: #1a1a2e; color: #e0e0e0; }"
  html = html + "canvas { background: #0f0f23; border: 1px solid #333; cursor: crosshair; }"
  html = html + ".container { display: flex; gap: 20px; flex-wrap: wrap; }"
  html = html + ".chart-box { background: #16213e; padding: 15px; border-radius: 8px; margin: 10px; }"
  html = html + ".info { padding: 10px; background: #0f3460; border-radius: 5px; margin: 5px 0; }"
  html = html + "button { padding: 8px 16px; margin: 5px; background: #e94560; color: white; border: none; border-radius: 4px; cursor: pointer; }"
  html = html + "button:hover { background: #c73e54; }"
  html = html + "</style></head><body>"
  html = html + "<h1>" + title + "</h1>"
  html = html + body_content
  html = html + extra_js
  html = html + "</body></html>"
  html

# ── Orbital Visualization ──
# Creates an HTML page showing particle positions, trails, and energy chart

fn orbital_viz_html(particles_data, energy_history, title)
  let canvas_w = 600
  let canvas_h = 600
  let body = "<div class='container'>"
  body = body + "<div class='chart-box'>"
  body = body + "<canvas id='orbitCanvas' width='" + str(canvas_w) + "' height='" + str(canvas_h) + "'></canvas>"
  body = body + "</div>"
  body = body + "<div class='chart-box'>"
  body = body + "<canvas id='energyChart' width='400' height='300'></canvas>"
  body = body + "</div>"
  body = body + "</div>"

  let js_data = "const particleData = " + json_stringify(particles_data) + ";"
  let js_energy = "const energyData = " + json_stringify(energy_history) + ";"

  let js = "<script>"
  js = js + js_data
  js = js + js_energy
  js = js + "const canvas = document.getElementById('orbitCanvas');"
  js = js + "const ctx = canvas.getContext('2d');"
  js = js + "const energyCtx = document.getElementById('energyChart').getContext('2d');"
  js = js + "function draw() {"
  js = js + "ctx.clearRect(0, 0, canvas.width, canvas.height);"
  js = js + "for (let p of particleData) {"
  js = js + "const scale = 20;"
  js = js + "const x = p.x * scale + canvas.width / 2;"
  js = js + "const y = canvas.height / 2 - p.y * scale;"
  js = js + "ctx.fillStyle = p.color;"
  js = js + "ctx.beginPath();"
  js = js + "ctx.arc(x, y, Math.max(p.radius, 3), 0, 6.28);"
  js = js + "ctx.fill();"
  js = js + "ctx.fillStyle = '#fff';"
  js = js + "ctx.font = '12px monospace';"
  js = js + "ctx.fillText(p.name, x + 10, y - 10);"
  js = js + "}"
  js = js + "drawEnergyChart();"
  js = js + "}"
  js = js + "function drawEnergyChart() {"
  js = js + "energyCtx.clearRect(0, 0, 400, 300);"
  js = js + "energyCtx.fillStyle = '#16213e';"
  js = js + "energyCtx.fillRect(0, 0, 400, 300);"
  js = js + "if (energyData.length < 2) return;"
  js = js + "const minE = Math.min.apply(null, energyData);"
  js = js + "const maxE = Math.max.apply(null, energyData);"
  js = js + "const range = maxE - minE || 1;"
  js = js + "energyCtx.strokeStyle = '#e94560';"
  js = js + "energyCtx.lineWidth = 2;"
  js = js + "energyCtx.beginPath();"
  js = js + "for (let i = 0; i < energyData.length; i++) {"
  js = js + "const x = 40 + (i / (energyData.length - 1)) * 340;"
  js = js + "const y = 270 - ((energyData[i] - minE) / range) * 220;"
  js = js + "if (i === 0) energyCtx.moveTo(x, y);"
  js = js + "else energyCtx.lineTo(x, y);"
  js = js + "}"
  js = js + "energyCtx.stroke();"
  js = js + "energyCtx.fillStyle = '#e0e0e0';"
  js = js + "energyCtx.font = '14px monospace';"
  js = js + "energyCtx.fillText('Energy Conservation', 140, 20);"
  js = js + "energyCtx.fillText('Initial: ' + energyData[0], 10, 290);"
  js = js + "energyCtx.fillText('Final: ' + energyData[energyData.length-1], 200, 290);"
  js = js + "}"
  js = js + "draw();"
  js = js + "</script>"

  html_page(title, body, js)

# ── Rocket Visualization ──
# Creates an HTML page showing rocket cross-section, thrust curve, and trajectory

fn rocket_viz_html(rocket_data, trajectory_data, thrust_data, title)
  let body = "<div class='container'>"
  body = body + "<div class='chart-box'>"
  body = body + "<canvas id='rocketCanvas' width='300' height='500'></canvas>"
  body = body + "</div>"
  body = body + "<div class='chart-box'>"
  body = body + "<canvas id='thrustChart' width='400' height='300'></canvas>"
  body = body + "</div>"
  body = body + "<div class='chart-box'>"
  body = body + "<canvas id='trajectoryChart' width='400' height='300'></canvas>"
  body = body + "</div>"
  body = body + "</div>"

  let js_data = "const rocketData = " + json_stringify(rocket_data) + ";"
  let js_traj = "const trajectoryData = " + json_stringify(trajectory_data) + ";"
  let js_thrust = "const thrustData = " + json_stringify(thrust_data) + ";"

  let js = "<script>"
  js = js + js_data + js_traj + js_thrust
  js = js + "const rCtx = document.getElementById('rocketCanvas').getContext('2d');"
  js = js + "const thrustCtx = document.getElementById('thrustChart').getContext('2d');"
  js = js + "const trajCtx = document.getElementById('trajectoryChart').getContext('2d');"
  js = js + "function drawRocket() {"
  js = js + "rCtx.clearRect(0, 0, 300, 500);"
  js = js + "let y = 450;"
  js = js + "const stages = rocketData.stages || [];"
  js = js + "for (let i = 0; i < stages.length; i++) {"
  js = js + "const s = stages[i];"
  js = js + "const h = 80;"
  js = js + "const w = 40;"
  js = js + "rCtx.fillStyle = s.color || '#e94560';"
  js = js + "rCtx.fillRect(130, y - h, w, h);"
  js = js + "rCtx.strokeStyle = '#fff';"
  js = js + "rCtx.lineWidth = 2;"
  js = js + "rCtx.strokeRect(130, y - h, w, h);"
  js = js + "rCtx.fillStyle = '#aaa';"
  js = js + "rCtx.fillRect(140, y, 20, 20);"
  js = js + "rCtx.fillStyle = '#fff';"
  js = js + "rCtx.font = '12px monospace';"
  js = js + "rCtx.fillText(s.name + ' (m=' + s.mass + 'kg)', 10, y - h + 15);"
  js = js + "rCtx.fillText('Isp=' + s.isp + 's', 10, y - h + 30);"
  js = js + "y -= h + 10;"
  js = js + "}"
  js = js + "rCtx.fillStyle = '#00d4ff';"
  js = js + "rCtx.fillRect(140, y, 20, 30);"
  js = js + "rCtx.strokeStyle = '#fff';"
  js = js + "rCtx.strokeRect(140, y, 20, 30);"
  js = js + "rCtx.fillStyle = '#fff';"
  js = js + "rCtx.fillText('Payload: ' + rocketData.payload + 'kg', 10, y + 15);"
  js = js + "}"
  js = js + "function drawThrustChart() {"
  js = js + "thrustCtx.clearRect(0, 0, 400, 300);"
  js = js + "thrustCtx.fillStyle = '#16213e';"
  js = js + "thrustCtx.fillRect(0, 0, 400, 300);"
  js = js + "if (thrustData.length < 2) return;"
  js = js + "let maxT = 0;"
  js = js + "for (let d of thrustData) { if (d.thrust > maxT) maxT = d.thrust; }"
  js = js + "if (maxT === 0) maxT = 1;"
  js = js + "thrustCtx.strokeStyle = '#00d4ff';"
  js = js + "thrustCtx.lineWidth = 2;"
  js = js + "thrustCtx.beginPath();"
  js = js + "for (let i = 0; i < thrustData.length; i++) {"
  js = js + "const x = 40 + (i / (thrustData.length - 1)) * 340;"
  js = js + "const y = 270 - (thrustData[i].thrust / maxT) * 220;"
  js = js + "if (i === 0) thrustCtx.moveTo(x, y);"
  js = js + "else thrustCtx.lineTo(x, y);"
  js = js + "}"
  js = js + "thrustCtx.stroke();"
  js = js + "thrustCtx.fillStyle = '#e0e0e0';"
  js = js + "thrustCtx.font = '14px monospace';"
  js = js + "thrustCtx.fillText('Thrust Curve (N)', 150, 20);"
  js = js + "}"
  js = js + "function drawTrajectory() {"
  js = js + "trajCtx.clearRect(0, 0, 400, 300);"
  js = js + "trajCtx.fillStyle = '#16213e';"
  js = js + "trajCtx.fillRect(0, 0, 400, 300);"
  js = js + "if (trajectoryData.length < 2) return;"
  js = js + "let maxAlt = 0; let maxVel = 0; let maxTime = 0;"
  js = js + "for (let d of trajectoryData) {"
  js = js + "if (d.altitude > maxAlt) maxAlt = d.altitude;"
  js = js + "if (d.velocity > maxVel) maxVel = d.velocity;"
  js = js + "if (d.time > maxTime) maxTime = d.time;"
  js = js + "}"
  js = js + "if (maxAlt === 0) maxAlt = 1;"
  js = js + "if (maxVel === 0) maxVel = 1;"
  js = js + "if (maxTime === 0) maxTime = 1;"
  js = js + "trajCtx.strokeStyle = '#e94560';"
  js = js + "trajCtx.lineWidth = 2;"
  js = js + "trajCtx.beginPath();"
  js = js + "for (let i = 0; i < trajectoryData.length; i++) {"
  js = js + "const x = 40 + (trajectoryData[i].time / maxTime) * 340;"
  js = js + "const y = 270 - (trajectoryData[i].altitude / maxAlt) * 220;"
  js = js + "if (i === 0) trajCtx.moveTo(x, y);"
  js = js + "else trajCtx.lineTo(x, y);"
  js = js + "}"
  js = js + "trajCtx.stroke();"
  js = js + "trajCtx.strokeStyle = '#00d4ff';"
  js = js + "trajCtx.beginPath();"
  js = js + "for (let i = 0; i < trajectoryData.length; i++) {"
  js = js + "const x = 40 + (trajectoryData[i].time / maxTime) * 340;"
  js = js + "const y = 270 - (trajectoryData[i].velocity / maxVel) * 220;"
  js = js + "if (i === 0) trajCtx.moveTo(x, y);"
  js = js + "else trajCtx.lineTo(x, y);"
  js = js + "}"
  js = js + "trajCtx.stroke();"
  js = js + "trajCtx.fillStyle = '#e0e0e0';"
  js = js + "trajCtx.font = '14px monospace';"
  js = js + "trajCtx.fillText('Trajectory (red=alt, blue=vel)', 100, 20);"
  js = js + "}"
  js = js + "drawRocket();"
  js = js + "drawThrustChart();"
  js = js + "drawTrajectory();"
  js = js + "</script>"

  html_page(title, body, js)

# ── Flight Visualization ──
# Creates an HTML page showing airplane flight dynamics

fn flight_viz_html(flight_data, title)
  let body = "<div class='chart-box'>"
  body = body + "<canvas id='flightCanvas' width='600' height='400'></canvas>"
  body = body + "</div>"

  let js_data = "const flightData = " + json_stringify(flight_data) + ";"

  let js = "<script>"
  js = js + js_data
  js = js + "const canvas = document.getElementById('flightCanvas');"
  js = js + "const ctx = canvas.getContext('2d');"
  js = js + "function draw() {"
  js = js + "ctx.clearRect(0, 0, 600, 400);"
  js = js + "const grad = ctx.createLinearGradient(0, 0, 0, 300);"
  js = js + "grad.addColorStop(0, '#4a90d9');"
  js = js + "grad.addColorStop(1, '#87ceeb');"
  js = js + "ctx.fillStyle = grad;"
  js = js + "ctx.fillRect(0, 0, 600, 300);"
  js = js + "ctx.fillStyle = '#2d5016';"
  js = js + "ctx.fillRect(0, 300, 600, 100);"
  js = js + "if (flightData.length < 2) return;"
  js = js + "let maxAlt = 0;"
  js = js + "for (let d of flightData) { if (d.altitude > maxAlt) maxAlt = d.altitude; }"
  js = js + "if (maxAlt === 0) maxAlt = 1;"
  js = js + "ctx.strokeStyle = '#fff';"
  js = js + "ctx.lineWidth = 2;"
  js = js + "ctx.beginPath();"
  js = js + "for (let i = 0; i < flightData.length; i++) {"
  js = js + "const x = 40 + (i / (flightData.length - 1)) * 500;"
  js = js + "const y = 290 - (flightData[i].altitude / maxAlt) * 200;"
  js = js + "if (i === 0) ctx.moveTo(x, y);"
  js = js + "else ctx.lineTo(x, y);"
  js = js + "}"
  js = js + "ctx.stroke();"
  js = js + "const last = flightData[flightData.length - 1];"
  js = js + "const ax = 40 + ((flightData.length - 1) / (flightData.length - 1)) * 500;"
  js = js + "const ay = 290 - (last.altitude / maxAlt) * 200;"
  js = js + "ctx.save();"
  js = js + "ctx.translate(ax, ay);"
  js = js + "ctx.fillStyle = '#ff6b6b';"
  js = js + "ctx.beginPath();"
  js = js + "ctx.moveTo(0, 0);"
  js = js + "ctx.lineTo(-20, 10);"
  js = js + "ctx.lineTo(20, 0);"
  js = js + "ctx.lineTo(-20, -10);"
  js = js + "ctx.closePath();"
  js = js + "ctx.fill();"
  js = js + "ctx.restore();"
  js = js + "ctx.fillStyle = '#fff';"
  js = js + "ctx.font = '14px monospace';"
  js = js + "ctx.fillText('Flight: ' + last.name, 10, 20);"
  js = js + "ctx.fillText('Alt: ' + last.altitude + 'm  Speed: ' + last.velocity + 'm/s', 10, 40);"
  js = js + "ctx.fillText('AoA: ' + last.alpha + 'rad  Lift: ' + last.lift + 'N', 10, 60);"
  js = js + "}"
  js = js + "draw();"
  js = js + "</script>"

  html_page(title, body, js)

# ── Serve Visualization ──
# Starts a web server to serve the visualization

fn serve_viz(html_content, port)
  say("Starting visualization server on port " + str(port))
  say("Open http://localhost:" + str(port) + " in your browser")
  let routes = {
    "/": html_content
  }
  serve(port, routes)

# ── Save Visualization to File ──
# Saves HTML content to a file using json_save

fn save_viz(html_content, filename)
  json_save(filename, {"html": html_content, "type": "visualization"})
  say("Visualization saved to " + filename + " (as JSON with 'html' field)")
  say("Open the file and extract the 'html' field, or use serve_viz() to serve it live")
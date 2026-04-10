import os

html_content = open("code.html", "r", encoding="utf-8").read()

# Make input and button identifiable
html_content = html_content.replace(
    '<input class="w-full bg-surface-container-lowest border-none',
    '<input id="city-input" class="w-full bg-surface-container-lowest border-none'
)
html_content = html_content.replace(
    '<button class="w-full md:w-auto bg-primary text-on-primary-fixed px-8 py-4 rounded-2xl',
    '<button id="analyze-btn" class="w-full md:w-auto bg-primary text-on-primary-fixed px-8 py-4 rounded-2xl'
)

# Values
html_content = html_content.replace(
    '<div class="text-4xl font-headline font-bold text-on-background">38.4<span class="text-primary text-2xl ml-1">°C</span></div>',
    '<div class="text-4xl font-headline font-bold text-on-background"><span id="val-temp">--</span><span class="text-primary text-2xl ml-1">°C</span></div>'
)

html_content = html_content.replace(
    '<div class="text-4xl font-headline font-bold text-on-background">64<span class="text-secondary text-2xl ml-1">%</span></div>',
    '<div class="text-4xl font-headline font-bold text-on-background"><span id="val-humidity">--</span><span class="text-secondary text-2xl ml-1">%</span></div>'
)

html_content = html_content.replace(
    '<div class="text-4xl font-headline font-bold text-on-background">42</div>',
    '<div class="text-4xl font-headline font-bold text-on-background" id="val-aqi">--</div>'
)

html_content = html_content.replace(
    '<span class="text-4xl font-headline font-bold text-on-background">72</span>',
    '<span class="text-4xl font-headline font-bold text-on-background" id="val-risk">--</span>'
)

html_content = html_content.replace(
    '<div class="text-4xl font-headline font-bold text-on-background">10000</div>',
    '<div class="text-4xl font-headline font-bold text-on-background" id="val-density">--</div>'
)

html_content = html_content.replace(
    '<span class="px-4 py-1 rounded-full bg-gradient-to-r from-error to-error-container text-on-primary-fixed text-xs font-bold uppercase tracking-wider">High Risk</span>',
    '<span id="val-risk-text" class="px-4 py-1 rounded-full bg-gradient-to-r from-error to-error-container text-on-primary-fixed text-xs font-bold uppercase tracking-wider">Ready</span>'
)

script = """
<script>
let map;
let markers = [];

async function toggleMap(show) {
    const overlay = document.getElementById('map-overlay');
    if (!overlay) return;
    if (show) {
        overlay.classList.remove('hidden');
        setTimeout(() => overlay.style.opacity = '1', 10);
        if (!map) initMap();
        loadMapData();
    } else {
        overlay.style.opacity = '0';
        setTimeout(() => overlay.classList.add('hidden'), 500);
    }
}

function initMap() {
    map = L.map('map', {
        zoomControl: false,
        attributionControl: false
    }).setView([20.5937, 78.9629], 5); // Center on India

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19
    }).addTo(map);
    
    L.control.zoom({ position: 'bottomright' }).addTo(map);
}

async function loadMapData() {
    const input = document.getElementById('city-input');
    const citySearch = input ? input.value : '';
    
    if (!citySearch) {
        // If no city entered, don't show markers or center on a default (like India)
        map.setView([20.5937, 78.9629], 5);
        return;
    }

    try {
        const response = await fetch(`/get-risk?city=${encodeURIComponent(citySearch)}`);
        const city = await response.json();
        
        if (city.error) return;

        // Clear old markers
        markers.forEach(m => map.removeLayer(m));
        markers = [];

        const color = city.risk_level === 'Low' ? '#83e881' : (city.risk_level === 'Medium' ? '#feb300' : '#ff716c');
        const radius = 15;

        // Center map and zoom smoothly
        map.flyTo([city.lat, city.lon], 10, {
            animate: true,
            duration: 1.5
        });

        // Glow effect
        const glow = L.circleMarker([city.lat, city.lon], {
            radius: radius + 8,
            fillColor: color,
            color: 'transparent',
            fillOpacity: 0.2
        }).addTo(map);

        const marker = L.circleMarker([city.lat, city.lon], {
            radius: radius,
            fillColor: color,
            color: '#fff',
            weight: 3,
            opacity: 1,
            fillOpacity: 0.9,
            className: 'marker-glow'
        }).addTo(map);

        const popupContent = `
            <div class="relative p-7 min-w-[320px] bg-surface-container/95 backdrop-blur-2xl rounded-[2.5rem] border border-outline-variant/20 shadow-[0_20px_60px_rgba(0,0,0,0.7)] animate-fade-up">
                <!-- POPUP CLOSE BUTTON -->
                <button onclick="map.closePopup()" class="absolute top-6 right-6 text-on-surface-variant/40 hover:text-error transition-colors p-1 group">
                    <span class="material-symbols-outlined text-xl group-hover:rotate-90 transition-transform">close</span>
                </button>

                <div class="mb-6 border-b border-outline-variant/10 pb-4">
                    <div class="flex items-center gap-3 mb-1">
                        <div class="w-2.5 h-2.5 rounded-full bg-primary animate-pulse shadow-[0_0_8px_#ff906d]"></div>
                        <h4 class="text-3xl font-headline font-extrabold text-on-background tracking-tight uppercase">${city.city}</h4>
                    </div>
                    <p class="text-[10px] font-bold uppercase tracking-[0.25em] text-on-surface-variant/50">Real-Time Risk Intelligence</p>
                </div>
                
                <div class="grid grid-cols-2 gap-y-5 gap-x-8">
                    <div class="flex flex-col gap-1.5">
                        <span class="text-[10px] font-black uppercase tracking-widest text-on-surface-variant/40 flex items-center gap-2">
                            <span class="material-symbols-outlined text-sm text-primary">device_thermostat</span> Temp
                        </span>
                        <span class="text-xl font-headline font-black text-primary">${city.temperature}<span class="text-xs ml-0.5 opacity-60">°C</span></span>
                    </div>
                    <div class="flex flex-col gap-1.5 text-right">
                        <span class="text-[10px] font-black uppercase tracking-widest text-on-surface-variant/40 flex items-center gap-2 justify-end">
                            <span class="material-symbols-outlined text-sm text-secondary">humidity_percentage</span> Humidity
                        </span>
                        <span class="text-xl font-headline font-black text-secondary">${city.humidity}<span class="text-xs ml-0.5 opacity-60">%</span></span>
                    </div>
                    <div class="flex flex-col gap-1.5">
                        <span class="text-[10px] font-black uppercase tracking-widest text-on-surface-variant/40 flex items-center gap-2">
                            <span class="material-symbols-outlined text-sm text-tertiary">air</span> AQI
                        </span>
                        <span class="text-xl font-headline font-black text-tertiary">${city.aqi}</span>
                    </div>
                    <div class="flex flex-col gap-1.5 text-right">
                        <span class="text-[10px] font-black uppercase tracking-widest text-on-surface-variant/40 flex items-center gap-2 justify-end">
                            <span class="material-symbols-outlined text-sm text-error">thermostat</span> Heat Index
                        </span>
                        <span class="text-xl font-headline font-black text-error">${city.heat_index.toFixed(1)}<span class="text-xs ml-0.5 opacity-60">°C</span></span>
                    </div>
                </div>

                <div class="mt-8 pt-6 border-t border-outline-variant/10 flex items-center justify-between">
                    <div class="flex flex-col gap-0.5">
                        <span class="text-[9px] font-black uppercase tracking-widest text-on-surface-variant/30">Total Risk</span>
                        <span class="text-3xl font-headline font-black text-on-background" style="color:${color}">${city.risk_score.toFixed(1)}</span>
                    </div>
                    <div class="px-6 py-3 rounded-2xl shadow-xl flex items-center gap-2 border border-white/5 active:scale-95 transition-transform cursor-default" style="background: linear-gradient(135deg, ${color}, ${color}dd);">
                         <span class="text-[12px] font-black uppercase tracking-[0.2em] text-on-primary-fixed">${city.risk_level} Risk</span>
                    </div>
                </div>
            </div>
        `;
        marker.bindPopup(popupContent).openPopup();
        markers.push(glow, marker);

    } catch (e) {
        console.error("Map load error:", e);
    }
}

async function executeRiskAnalysis() {
    const city = document.getElementById('city-input').value;
    if (!city) return;
    
    // UI Loading state
    document.getElementById('analyze-btn').innerText = "Calculating...";
    
    const grid = document.getElementById('results-grid');
    const spinner = document.getElementById('loading-spinner');
    const errorBanner = document.getElementById('error-banner');
    const errorText = document.getElementById('error-text');
    
    errorBanner.classList.add('hidden');
    errorBanner.classList.remove('flex');
    errorBanner.style.opacity = '0';
    
    grid.style.opacity = '0';
    setTimeout(() => {
        grid.classList.add('hidden');
        spinner.classList.remove('hidden');
        spinner.classList.add('flex');
        void spinner.offsetWidth;
        spinner.style.opacity = '1';
    }, 300);
    
    try {
        const response = await fetch(`/get-risk?city=${encodeURIComponent(city)}`);
        const data = await response.json();
        
        if (data.error) {
            setTimeout(() => {
                spinner.style.opacity = '0';
                setTimeout(() => {
                    spinner.classList.add('hidden');
                    spinner.classList.remove('flex');
                    errorText.innerText = data.error;
                    errorBanner.classList.remove('hidden');
                    errorBanner.classList.add('flex');
                    void errorBanner.offsetWidth;
                    errorBanner.style.opacity = '1';
                    
                    grid.classList.remove('hidden');
                    void grid.offsetWidth;
                    grid.style.opacity = '1';
                }, 300);
            }, 500);
        } else {
            document.getElementById('val-temp').innerText = data.temperature;
            document.getElementById('val-humidity').innerText = data.humidity;
            document.getElementById('val-aqi').innerText = data.aqi;
            if (document.getElementById('val-risk')) {
                 document.getElementById('val-risk').innerText = data.risk_score.toFixed(1);
            }
            if (document.getElementById('val-hi')) {
                document.getElementById('val-hi').innerText = data.heat_index.toFixed(1);
            }
            
            if(document.getElementById('calc-step1-temp')) {
                document.getElementById('calc-step1-temp').innerText = data.temperature;
                document.getElementById('calc-step1-hum').innerText = data.humidity;
                document.getElementById('calc-step1-result').innerText = data.heat_index.toFixed(1);
                
                document.getElementById('calc-step2-hi').innerText = data.heat_index.toFixed(1);
                document.getElementById('calc-step2-aqi').innerText = data.aqi;
                document.getElementById('calc-step2-den').innerText = (data.density / 10000).toFixed(2);
                document.getElementById('calc-step2-result').innerText = data.risk_score.toFixed(1);
                
                document.getElementById('calc-final-hi').innerText = data.heat_index.toFixed(1);
                document.getElementById('calc-final-rs').innerText = data.risk_score.toFixed(1);
                
                const levelText = document.getElementById('calc-final-level');
                levelText.innerText = data.risk_level;
                if(data.risk_level === 'Low') {
                    levelText.className = "px-5 py-2 rounded-full bg-gradient-to-r from-tertiary to-tertiary-dim text-on-primary-fixed text-sm font-bold uppercase tracking-wider shadow-inner";
                } else if(data.risk_level === 'Medium') {
                    levelText.className = "px-5 py-2 rounded-full bg-gradient-to-r from-secondary to-secondary-dim text-on-primary-fixed text-sm font-bold uppercase tracking-wider shadow-inner";
                } else {
                    levelText.className = "px-5 py-2 rounded-full bg-gradient-to-r from-error to-error-container text-on-primary-fixed text-sm font-bold uppercase tracking-wider shadow-inner";
                }
            }

            const riskText = document.getElementById('val-risk-text');
            if (riskText) {
                riskText.innerText = data.risk_level;
                if(data.risk_level === 'Low') {
                    riskText.className = "px-4 py-1 rounded-full bg-gradient-to-r from-tertiary to-tertiary-dim text-on-primary-fixed text-xs font-bold uppercase tracking-wider";
                } else if(data.risk_level === 'Medium') {
                    riskText.className = "px-4 py-1 rounded-full bg-gradient-to-r from-secondary to-secondary-dim text-on-primary-fixed text-xs font-bold uppercase tracking-wider";
                } else {
                    riskText.className = "px-4 py-1 rounded-full bg-gradient-to-r from-error to-error-container text-on-primary-fixed text-xs font-bold uppercase tracking-wider";
                }
            }
            setTimeout(() => {
                spinner.style.opacity = '0';
                setTimeout(() => {
                    spinner.classList.add('hidden');
                    spinner.classList.remove('flex');
                    
                    grid.classList.remove('hidden');
                    void grid.offsetWidth;
                    grid.style.opacity = '1';
                }, 300);
            }, 500);
        }
    } catch(e) {
        setTimeout(() => {
            spinner.style.opacity = '0';
            setTimeout(() => {
                spinner.classList.add('hidden');
                spinner.classList.remove('flex');
                
                errorText.innerText = "Unable to fetch data";
                errorBanner.classList.remove('hidden');
                errorBanner.classList.add('flex');
                void errorBanner.offsetWidth;
                errorBanner.style.opacity = '1';
                
                grid.classList.remove('hidden');
                void grid.offsetWidth;
                grid.style.opacity = '1';
            }, 300);
        }, 500);
    }
    
    document.getElementById('analyze-btn').innerHTML = '<span class="material-symbols-outlined">analytics</span> Check Risk';
}

document.getElementById('analyze-btn').addEventListener('click', executeRiskAnalysis);
document.getElementById('city-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        executeRiskAnalysis();
    }
});

const mapBtn = document.getElementById('view-map-btn');
if(mapBtn) mapBtn.addEventListener('click', () => toggleMap(true));

const closeMapBtn = document.getElementById('close-map-btn');
if(closeMapBtn) closeMapBtn.addEventListener('click', () => toggleMap(false));
</script>
</body>
"""

html_content = html_content.replace('</body>', script)

os.makedirs('templates', exist_ok=True)
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

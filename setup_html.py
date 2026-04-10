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
</script>
</body>
"""

html_content = html_content.replace('</body>', script)

os.makedirs('templates', exist_ok=True)
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

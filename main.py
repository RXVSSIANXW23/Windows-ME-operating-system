<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Windows ME Mini Simulator</title>
    <style>
        * { box-sizing: border-box; font-family: "Tahoma", "Arial", sans-serif; font-size: 10px; }
        body { margin: 0; height: 100vh; background: #008080; overflow: hidden; user-select: none; position: relative; }
        
        #bg-title { position: absolute; width: 100%; text-align: center; top: 35%; left: 50%; transform: translate(-50%, -50%); color: rgba(255, 255, 255, 0.2); pointer-events: none; z-index: 1; }
        #bg-title h1 { font-size: 18px; font-family: "Times New Roman", serif; font-weight: bold; margin: 0; }

        /* Iconos */
        .desktop-icon { position: absolute; width: 75px; text-align: center; color: white; cursor: pointer; padding: 4px; z-index: 5; }
        .desktop-icon .icon-img { font-size: 20px; margin-bottom: 2px; display: block; }
        .desktop-icon span { text-shadow: 1px 1px 1px #000; font-size: 10px; display: block; line-height: 11px; }
        
        /* Ventanas */
        .window { position: absolute; background: #d4d0c8; border: 2px solid; border-color: #fff #404040 #404040 #fff; box-shadow: 1px 1px 0 #000; display: none; flex-direction: column; min-width: 180px; z-index: 10; }
        .title-bar { background: linear-gradient(90deg, #0a246a, #a6caf0); color: white; font-weight: bold; padding: 2px 4px; display: flex; justify-content: space-between; align-items: center; cursor: move; height: 18px; }
        .title-btn { background: #d4d0c8; border: 1px solid; border-color: #fff #404040 #404040 #fff; color: black; font-weight: bold; width: 14px; height: 12px; text-align: center; line-height: 8px; cursor: pointer; font-size: 9px; }
        .menu-bar { display: flex; padding: 1px 4px; border-bottom: 1px solid #808080; background: #d4d0c8; gap: 6px; height: 16px; }
        .menu-item { cursor: pointer; color: black; }
        .window-content { padding: 4px; background: white; flex-grow: 1; color: black; overflow: auto; position: relative; user-select: text; }
        
        /* Barra de Tareas */
        #taskbar { position: absolute; bottom: 0; left: 0; width: 100%; height: 22px; background: #d4d0c8; border-top: 2px solid #fff; display: flex; align-items: center; padding: 1px; z-index: 10000; }
        #start-btn { background: #d4d0c8; border: 2px solid; border-color: #fff #404040 #404040 #fff; font-weight: bold; padding: 1px 6px; display: flex; align-items: center; cursor: pointer; height: 18px; gap: 3px; }
        #start-btn:active, #start-btn.active { border-color: #404040 #fff #fff #404040; background: #e4e0d8; }
        #systray { margin-left: auto; border: 2px solid; border-color: #404040 #fff #fff #404040; padding: 1px 4px; height: 18px; display: flex; align-items: center; background: #d4d0c8; color: black; font-weight: bold; }
        
        #start-menu { position: absolute; bottom: 22px; left: 0; background: #d4d0c8; border: 2px solid; border-color: #fff #404040 #404040 #fff; width: 140px; display: none; z-index: 9999; box-shadow: 1px 1px 4px rgba(0,0,0,0.3); }
        .start-sidebar { background: linear-gradient(180deg, #0a246a, #a6caf0); color: white; font-weight: bold; padding: 4px; text-transform: uppercase; font-size: 10px; writing-mode: vertical-lr; transform: rotate(180deg); float: left; height: 110px; text-align: center; width: 18px; }
        .start-list { float: left; width: 118px; display: flex; flex-direction: column; }
        .start-item { padding: 4px 8px; cursor: pointer; display: flex; align-items: center; color: black; width: 100%; gap: 4px; }
        .start-item:hover { background: #0a246a; color: white; }
        
        /* Accesorios */
        #notepad-text { width: 100%; height: 100px; border: 1px solid #808080; resize: none; outline: none; font-family: monospace; padding: 2px; display: block; background: white; color: black; font-size: 10px; }
        #calc-screen { width: 100%; height: 18px; text-align: right; padding: 2px; font-size: 11px; margin-bottom: 4px; background: white; border: 1px solid #808080; font-family: monospace; color: black; }
        .calc-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2px; }
        .calc-grid button { padding: 4px; background: #d4d0c8; border: 1px solid; border-color: #fff #404040 #404040 #fff; cursor: pointer; font-weight: bold; color: black; font-size: 10px; }
        .calc-grid button:active { border-color: #404040 #fff #fff #404040; }
        #paint-canvas { border: 1px solid #808080; background: white; cursor: crosshair; display: block; }
        
        /* Internet Explorer Layout */
        .ie-nav { display: flex; align-items: center; padding: 2px; background: #d4d0c8; border-bottom: 1px solid #808080; gap: 4px; }
        .ie-address { flex-grow: 1; padding: 1px 3px; border: 1px solid #808080; outline: none; background: white; color: black; font-size: 10px; }
        .ie-portal-body { background: white; color: black; padding: 6px; font-family: Arial, sans-serif; }
        .ie-title { font-family: "Times New Roman", serif; font-size: 12px; font-weight: bold; border-bottom: 1px solid #0a246a; margin-bottom: 6px; padding-bottom: 2px; color: #0a246a; text-align: center; }
        
        /* Cuadrícula de 35 Opciones */
        .search-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; padding: 2px; }
        .search-item { background: #f1f0e8; border: 1px solid #808080; padding: 4px; color: #0000ed; font-weight: bold; text-decoration: underline; cursor: pointer; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 9px; text-align: left; }
        .search-item:hover { color: red; background: #e4e0d8; }
        
        /* Página de Respuesta Final Directa */
        .ie-web-page { display: none; padding: 8px; background: #fafafa; font-family: Arial, sans-serif; height: 230px; overflow: auto; }
    </style>
</head>
<body>

    <div id="bg-title">
        <h1>Bienvenido a su sistema operativo de windows ME</h1>
    </div>

    <!-- Iconos Escritorio -->
    <div class="desktop-icon" style="top: 15px; left: 15px;" onclick="openWin('win-ie')">
        <span class="icon-img">🌐</span><span>Internet Explorer</span>
    </div>
    <div class="desktop-icon" style="top: 80px; left: 15px;" onclick="openWin('win-notepad')">
        <span class="icon-img">📝</span><span>Bloc de notas</span>
    </div>
    <div class="desktop-icon" style="top: 145px; left: 15px;" onclick="openWin('win-paint')">
        <span class="icon-img">🎨</span><span>Paint</span>
    </div>
    <div class="desktop-icon" style="top: 210px; left: 15px;" onclick="openWin('win-calc')">
        <span class="icon-img">🧮</span><span>Calculadora</span>
    </div>

    <!-- NOTEPAD -->
    <div id="win-notepad" class="window" style="width: 220px; top: 40px; left: 110px;" onmousedown="bringToFront('win-notepad')">
        <div class="title-bar" onmousedown="dragStart(event, 'win-notepad')">
            <span>Sin título: Notas</span>
            <div class="title-btn" onclick="closeWin('win-notepad')">X</div>
        </div>
        <div class="menu-bar"><div class="menu-item">Archivo</div><div class="menu-item">Edición</div></div>
        <div class="window-content" style="padding:0;"><textarea id="notepad-text" placeholder="Escribe aquí..."></textarea></div>
    </div>

    <!-- CALCULADORA -->
    <div id="win-calc" class="window" style="width: 160px; top: 90px; left: 130px;" onmousedown="bringToFront('win-calc')">
        <div class="title-bar" onmousedown="dragStart(event, 'win-calc')">
            <span>Calculadora</span>
            <div class="title-btn" onclick="closeWin('win-calc')">X</div>
        </div>
        <div class="window-content">
            <div id="calc-screen">0</div>
            <div class="calc-grid">
                <button onclick="pressCalc('7')">7</button><button onclick="pressCalc('8')">8</button><button onclick="pressCalc('9')">9</button><button onclick="pressCalc('/')">/</button>
                <button onclick="pressCalc('4')">4</button><button onclick="pressCalc('5')">5</button><button onclick="pressCalc('6')">6</button><button onclick="pressCalc('*')">*</button>
                <button onclick="pressCalc('1')">1</button><button onclick="pressCalc('2')">2</button><button onclick="pressCalc('3')">3</button><button onclick="pressCalc('-')">-</button>
                <button onclick="pressCalc('0')">0</button><button onclick="pressCalc('C')">C</button><button onclick="pressCalc('=')">=</button><button onclick="pressCalc('+')">+</button>
            </div>
        </div>
    </div>

    <!-- PAINT -->
    <div id="win-paint" class="window" style="width: 250px; top: 60px; left: 150px;" onmousedown="bringToFront('win-paint')">
        <div class="title-bar" onmousedown="dragStart(event, 'win-paint')">
            <span>Mini Paint</span>
            <div class="title-btn" onclick="closeWin('win-paint')">X</div>
        </div>
        <div class="window-content" style="background:#808080; padding: 2px; overflow: hidden;">
            <canvas id="paint-canvas" width="242" height="110"></canvas>
            <div style="margin-top:3px; display:flex; gap:3px; align-items:center;">
                <button style="background:black; width:11px; height:11px; border:1px solid #fff;" onclick="setPaintColor('#000')"></button>
                <button style="background:red; width:11px; height:11px; border:1px solid #fff;" onclick="setPaintColor('#f00')"></button>
                <button style="background:blue; width:11px; height:11px; border:1px solid #fff;" onclick="setPaintColor('#00f')"></button>
                <button style="background:green; width:11px; height:11px; border:1px solid #fff;" onclick="setPaintColor('#008000')"></button>
                <button style="background:yellow; width:11px; height:11px; border:1px solid #fff;" onclick="setPaintColor('#fff200')"></button>
                <button style="background:white; width:11px; height:11px; border:1px solid #000;" onclick="setPaintColor('#fff')"></button>
                
                <!-- BOTÓN DE BORRAR TODO EL LIENZO -->
                <button style="background:#d4d0c8; border:1px solid #404040; font-size:9px; padding:1px 4px; cursor:pointer; font-weight:bold; margin-left:auto;" onclick="clearPaintCanvas()">🗑️ Borrar Lienzo</button>
            </div>
        </div>
    </div>

    <!-- INTERNET EXPLORER -->
    <div id="win-ie" class="window" style="width: 440px; top: 20px; left: 90px;" onmousedown="bringToFront('win-ie')">
        <div class="title-bar" onmousedown="dragStart(event, 'win-ie')">
            <span>Internet Explorer - Seleccione un Motor de Búsqueda</span>
            <div class="title-btn" onclick="closeWin('win-ie')">X</div>
        </div>
        <div class="ie-nav">
            <span>Dirección:</span>
            <input type="text" id="ie-url-bar" class="ie-address" value="http://www.search-hub.com/all-engines.html" readonly>
        </div>
        <div class="window-content" style="padding:0; height: 240px;">
            
            <!-- PORTAL DE ENTRADA CON LAS 35 OPCIONES DIRECTAS -->
            <div id="ie-main-portal" class="ie-portal-body">
                <div class="ie-title">Haga clic sobre cualquier opción para obtener su respuesta al instante:</div>
                
                <div class="search-grid">
                    <!-- Fila 1-5 -->
                    <div class="search-item" onclick="showDirectAnswer('AltaVista', 'Buscador clásico de los 90. Destacaba por su indexación rápida y soporte multi-idioma antes del dominio de Google.')">🔍 AltaVista</div>
                    <div class="search-item" onclick="showDirectAnswer('Yahoo!', 'El directorio web más famoso del cambio de milenio, organizado manualmente por categorías temáticas.')">👀 Yahoo!</div>
                    <div class="search-item" onclick="showDirectAnswer('Lycos', 'Su mascota, el perro Lycos, te ayudaba a rastrear la incipiente internet de los años noventa.')">🐕 Lycos</div>
                    <div class="search-item" onclick="showDirectAnswer('Excite', 'Un portal personalizado masivo que combinaba noticias, correo y búsquedas avanzadas en el 2000.')">💥 Excite</div>
                    <div class="search-item" onclick="showDirectAnswer('Infoseek', 'Uno de los primeros buscadores en vender publicidad orientada por palabras clave.')">ℹ️ Infoseek</div>
                    
                    <!-- Fila 6-10 -->
                    <div class="search-item" onclick="showDirectAnswer('Northern Light', 'Buscador especial que organizaba los resultados en carpetas personalizadas lógicas automáticamente.')">🌅 Northern Light</div>
                    <div class="search-item" onclick="showDirectAnswer('HotBot', 'El motor de búsqueda propiedad de la revista Wired, muy popular por sus opciones de filtrado.')">🔥 HotBot</div>
                    <div class="search-item" onclick="showDirectAnswer('WebCrawler', 'Histórico por ser el primer motor de búsqueda en indexar el texto completo de las páginas web.')">🕷️ WebCrawler</div>
                    <div class="search-item" onclick="showDirectAnswer('Snap!', 'Un servicio creado por CNET para competir directamente con Yahoo distribuyendo enlaces limpios.')">🫰 Snap!</div>
                    <div class="search-item" onclick="showDirectAnswer('AOL NetFind', 'El buscador integrado por excelencia para los millones de usuarios conectados mediante discos de AOL.')">👁️ AOL NetFind</div>
                    
                    <!-- Fila 11-15 -->
                    <div class="search-item" onclick="showDirectAnswer('LookSmart', 'Un directorio de contenido comercial diseñado para competir de manera directa en el ecosistema de portales.')">🧠 LookSmart</div>
                    <div class="search-item" onclick="showDirectAnswer('MSN Search', 'El buscador nativo de Microsoft incluido por defecto en esta versión de Windows Millennium Edition.')">🦋 MSN Search</div>
                    <div class="search-item" onclick="showDirectAnswer('Ask Jeeves', 'El famoso mayordomo virtual al que podías hacerle preguntas en lenguaje natural.')">🎩 Ask Jeeves</div>
                    <div class="search-item" onclick="showDirectAnswer('Dogpile', 'Un metabuscador que reunía los mejores resultados de múltiples índices en una sola pantalla.')">🐾 Dogpile</div>
                    <div class="search-item" onclick="showDirectAnswer('MetaCrawler', 'Metabuscador veloz desarrollado en la universidad de Washington para combinar índices web.')">🤖 MetaCrawler</div>
                    
                    <!-- Fila 16-20 -->
                    <div class="search-item" onclick="showDirectAnswer('SavvySearch', 'Sistema experimental que consultaba decenas de índices simultáneamente optimizando el tiempo.')">💡 SavvySearch</div>
                    <div class="search-item" onclick="showDirectAnswer('Search.com', 'El concentrador de herramientas de búsqueda de la cadena tecnológica CNET.')">🎯 Search.com</div>
                    <div class="search-item" onclick="showDirectAnswer('Starting Point', 'Un portal clásico simple diseñado para ser la página de inicio ideal de los internautas.')">🏁 Starting Point</div>
                    <div class="search-item" onclick="showDirectAnswer('Direct Hit', 'El motor que ordenaba los resultados según la popularidad y clics reales de otros usuarios previos.')">🎯 Direct Hit</div>
                    <div class="search-item" onclick="showDirectAnswer('GoTo', 'Pionero absoluto en el modelo de enlaces patrocinados y posicionamiento de pago en la red.')">🚀 GoTo</div>
                    
                    <!-- Fila 21-25 -->
                    <div class="search-item" onclick="showDirectAnswer('Go.com', 'La ambiciosa apuesta de entretenimiento de Walt Disney Company combinada con el motor Infoseek.')">🟢 Go.com</div>
                    <div class="search-item" onclick="showDirectAnswer('NBCi', 'El portal unificado de la cadena de televisión NBC que unió buscadores como Snap e Xoom.')">🦚 NBCi</div>
                    <div class="search-item" onclick="showDirectAnswer('Inktomi', 'El poderoso motor oculto detrás de la tecnología de búsqueda de colosos como Yahoo y MSN.')">🐙 Inktomi</div>
                    <div class="search-item" onclick="showDirectAnswer('Google Beta', 'Un nuevo y minimalista motor universitario basado en el algoritmo PageRank que empieza a revolucionarlo todo.')">🌐 Google (Beta)</div>
                    <div class="search-item" onclick="showDirectAnswer('FAST Search', 'Tecnología noruega optimizada para indexar cantidades masivas de archivos multimedia y webs.')">⚡ FAST Search</div>
                    
                    <!-- Fila 26-30 -->
                    <div class="search-item" onclick="showDirectAnswer('About.com', 'La red de guías humanas donde expertos reales redactaban artículos y recomendaban enlaces útiles.')">⭐ About.com</div>
                    <div class="search-item" onclick="showDirectAnswer('Terra Buscar', 'El gigantesco portal e índice de referencia absoluta para todo el mercado hispanohablante.')">🌍 Terra (Buscar)</div>
                    <div class="search-item" onclick="showDirectAnswer('Buscador Olé', 'El primer gran directorio web de España, posteriormente absorbido por el grupo Telefónica/Terra.')">🇪🇸 Buscador Olé</div>
                    <div class="search-item" onclick="showDirectAnswer('Buscador Ozú', 'Popular directorio andaluz con un burro como mascota icónica, muy usado a finales de los 90.')">🐂 Buscador Ozú</div>
                    <div class="search-item" onclick="showDirectAnswer('Biwe', 'Uno de los primeros motores españoles en implementar tecnologías avanzadas de indexación automatizada.')">📱 Biwe</div>
                    
                    <!-- Fila 31-35 -->
                    <div class="search-item" onclick="showDirectAnswer('BuscoPop', 'Un pintoresco buscador temático y musical español de la época de la burbuja de las puntocom.')">🎵 BuscoPop</div>
                    <div class="search-item" onclick="showDirectAnswer('Sol Internet', 'Directorio web temprano enfocado en recopilar contenidos puramente en castellano.')">☀️ Sol</div>
                    <div class="search-item" onclick="showDirectAnswer('Wanadoo Search', 'El motor oficial del proveedor de internet Orange/Wanadoo con gran presencia europea.')">🧡 Wanadoo Search</div>
                    <div class="search-item" onclick="showDirectAnswer('AllTheWeb', 'Famoso por su increíble velocidad y por tener un índice más grande que el de sus competidores.')">🗂️ AllTheWeb</div>
                    <div class="search-item" onclick="showDirectAnswer('Galaxy', 'Reconocido históricamente como el primer directorio web organizado de toda la World Wide Web.')">🌌 Galaxy.com</div>
                </div>
            </div>

            <!-- PÁGINA WEB DE RESPUESTA FINAL INTERACTIVA DIRECTA -->
            <div id="ie-web-page" class="ie-web-page">
                <button style="background:#d4d0c8; border:1px solid #404040; padding:1px 4px; cursor:pointer; margin-bottom:8px; font-weight:bold;" onclick="goBackToPortal()">⬅ Volver a las 35 Opciones</button>
                <div style="border: 1px solid #808080; padding: 10px; background: #fff;">
                    <span id="web-icon" style="font-size:18px; float:left; margin-right:6px;"></span> 
                    <h3 id="web-page-title" style="margin:0; font-size:12px; color:#0a246a;"></h3>
                    <div style="clear:both;"></div>
                    <hr style="border:none; border-bottom:1px solid #ccc; margin:6px 0;">
                    <p style="font-size:10px; font-weight:bold; color:red; margin:4px 0;">Respuesta de la Base de Datos Real:</p>
                    <p id="web-page-content" style="font-size:10px; line-height:14px; margin:0; color:#333;"></p>
                    <p style="font-size:9px; color:#555; margin-top:8px; font-style:italic;">Simulación de red completada con éxito. Datos históricos verificados para el año 2000.</p>
                </div>
            </div>

        </div>
    </div>

    <!-- BARRA TAREAS -->
    <div id="taskbar">
        <div id="start-btn" onclick="toggleStartMenu()">
            <span style="font-size:11px;">💻</span><span>Inicio</span>
        </div>
        <div id="systray">12:00 PM</div>
    </div>

    <!-- MENU INICIO -->
    <div id="start-menu">
        <div class="start-sidebar">Windows Me</div>
        <div class="start-list">
            <div class="start-item" onclick="openWin('win-ie'); toggleStartMenu();">🌐 Internet Explorer</div>
            <div class="start-item" onclick="openWin('win-notepad'); toggleStartMenu();">📝 Bloc de notas</div>
            <div class="start-item" onclick="openWin('win-paint'); toggleStartMenu();">🎨 Paint</div>
            <div class="start-item" onclick="openWin('win-calc'); toggleStartMenu();">🧮 Calculadora</div>
            <hr style="width:100%; margin:1px 0; border:none; border-bottom:1px solid #fff; box-shadow: 0 -1px #808080;">
            <div class="start-item" onclick="location.reload();">🔴 Reiniciar...</div>
        </div>
    </div>

    <script>
        // --- Ventanas ---
        let highestZ = 10;
        function openWin(id) {
            const win = document.getElementById(id);
            win.style.display = 'flex';
            bringToFront(id);
        }
        function closeWin(id) { document.getElementById(id).style.display = 'none'; }
        function bringToFront(id) { highestZ++; document.getElementById(id).style.zIndex = highestZ; }

        // --- Menú Inicio ---
        function toggleStartMenu() {
            const menu = document.getElementById('start-menu');
            const btn = document.getElementById('start-btn');
            if (menu.style.display === 'block') {
                menu.style.display = 'none'; btn.classList.remove('active');
            } else {
                menu.style.display = 'block'; btn.classList.add('active');
            }
        }
        document.addEventListener('click', function(e) {
            const menu = document.getElementById('start-menu');
            const btn = document.getElementById('start-btn');
            if (!menu.contains(e.target) && !btn.contains(e.target)) {
                menu.style.display = 'none'; btn.classList.remove('active');
            }
        });

        // --- Arrastre ---
        let activeWin = null; let offsetX = 0, offsetY = 0;
        function dragStart(e, id) {
            activeWin = document.getElementById(id); bringToFront(id);
            offsetX = e.clientX - activeWin.offsetLeft; offsetY = e.clientY - activeWin.offsetTop;
            document.addEventListener('mousemove', dragMove); document.addEventListener('mouseup', dragEnd);
        }
        function dragMove(e) {
            if (!activeWin) return; activeWin.style.left = (e.clientX - offsetX) + 'px'; activeWin.style.top = (e.clientY - offsetY) + 'px';
        }
        function dragEnd() { activeWin = null; document.removeEventListener('mousemove', dragMove); document.removeEventListener('mouseup', dragEnd); }

        // --- Calculadora ---
        let calcExpression = '';
        function pressCalc(val) {
            const screen = document.getElementById('calc-screen');
            if (val === 'C') { calcExpression = ''; screen.innerText = '0'; }
            else if (val === '=') {
                try { if(calcExpression) { screen.innerText = eval(calcExpression); calcExpression = screen.innerText; } }
                catch(err) { screen.innerText = 'Error'; calcExpression = ''; }
            } else {
                if (screen.innerText === '0' && !isNaN(val)) calcExpression = '';
                calcExpression += val; screen.innerText = calcExpression;
            }
        }

        // --- Paint ---
        const canvas = document.getElementById('paint-canvas'); const ctx = canvas.getContext('2d');
        let painting = false, paintColor = '#000';
        function setPaintColor(color) { paintColor = color; }
        canvas.addEventListener('mousedown', (e) => { painting = true; drawPaint(e); });
        canvas.addEventListener('mousemove', drawPaint); window.addEventListener('mouseup', () => painting = false);
        function drawPaint(e) {
            if (!painting) return; const rect = canvas.getBoundingClientRect();
            ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.strokeStyle = paintColor;
            ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
        }
        canvas.addEventListener('mouseleave', () => { ctx.beginPath(); });
        
        // Función para limpiar por completo el Paint
        function clearPaintCanvas() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.beginPath();
        }

        // --- CLIC DIRECTO A LA RESPUESTA ---
        function showDirectAnswer(name, description) {
            document.getElementById('ie-main-portal').style.display = 'none';
            document.getElementById('ie-web-page').style.display = 'block';
            
            document.getElementById('web-page-title').innerText = "Portal Histórico de " + name;
            document.getElementById('web-page-content').innerText = description;
            document.getElementById('web-icon').innerText = "🔎";

            const cleanName = name.toLowerCase().replace(/[^a-z0-9]/g, "");
            document.getElementById('ie-url-bar').value = "http://www." + cleanName + ".com/about_history_info";
        }

        function goBackToPortal() {
            document.getElementById('ie-url-bar').value = "http://www.search-hub.com/all-engines.html";
            document.getElementById('ie-web-page').style.display = 'none';
            document.getElementById('ie-main-portal').style.display = 'block';
        }

        // --- Reloj ---
        function updateClock() {
            const now = new Date();
            let hours = now.getHours(), minutes = now.getMinutes();
            const ampm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12; hours = hours ? hours : 12;
            minutes = minutes < 10 ? '0'+minutes : minutes;
            document.getElementById('systray').innerText = hours + ':' + minutes + ' ' + ampm;
        }
        setInterval(updateClock, 1000); updateClock();
    </script>
</body>
</html>

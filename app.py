<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tu Proyecto Final</title>
    <style>
        /* Estilos base para asegurar que se vea impecable */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            max-width: 500px;
            width: 100%;
        }

        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 1.5rem;
        }

        .input-group {
            margin-bottom: 1rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }

        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            box-sizing: border-box; /* Evita que el input se salga del contenedor */
        }

        button {
            width: 100%;
            padding: 12px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.3s ease;
        }

        button:hover {
            background-color: #0056b3;
        }

        #resultado {
            margin-top: 1.5rem;
            padding: 1rem;
            border-radius: 6px;
            text-align: center;
            font-weight: bold;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Configuración Exacta</h1>
    
    <div class="input-group">
        <label for="dato">Ingresa el valor:</label>
        <input type="text" id="dato" placeholder="Escribe aquí...">
    </div>

    <button onclick="procesarDato()">EJECUTAR AHORA</button>

    <div id="resultado"></div>
</div>

<script>
    function procesarDato() {
        const input = document.getElementById('dato');
        const display = document.getElementById('resultado');
        const valor = input.value.trim();

        if (valor === "") {
            display.style.color = "red";
            display.innerHTML = "⚠️ Por favor, escribe algo primero.";
        } else {
            display.style.color = "green";
            display.innerHTML = `✅ Procesado con éxito: "${valor}"`;
            console.log("Dato recibido:", valor);
        }
    }
</script>

</body>
</html>

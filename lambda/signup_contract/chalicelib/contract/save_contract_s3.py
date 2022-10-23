#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from chalicelib.utils import dynamo_utils, s3_utils
from chalicelib.data import config
table_name = 'pulsar_retargeting'

HTML_TEXT = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solicitar firma de usuario</title>
    <link rel="stylesheet" href="estilo.css">
</head>

<body>
    <h1 align="center">Este es tu contrato {} </h1>
    <hr>
    <p>CONTRATO DE TARJETA DE CREDITO QUE CELEBRAN, POR UNA PARTE BBVA COLOMBIA Y
        POR LA OTRA PARTE Y POR SU PROPIO DERECHO,<b> {} {} {}</b></p>
    <p>Firmar a continuación:</p>
    <canvas id="canvas"></canvas>
    <br>
    <button id="btnLimpiar">Limpiar</button>
    <button id="btnGenerarDocumento">Pasar a documento</button>
    <br>
    <script src="script.js"></script>
</body>

</html>
"""

STYLE_CSS = """
#canvas {
    border: 1px solid black;
}
"""

JS_TEXT = """
/**/
const $canvas = document.querySelector("#canvas"),
    $btnLimpiar = document.querySelector("#btnLimpiar"),
    $btnGenerarDocumento = document.querySelector("#btnGenerarDocumento");
const contexto = $canvas.getContext("2d");
const COLOR_PINCEL = "black";
const COLOR_FONDO = "white";
const GROSOR = 2;
let xAnterior = 0, yAnterior = 0, xActual = 0, yActual = 0;
const obtenerXReal = (clientX) => clientX - $canvas.getBoundingClientRect().left;
const obtenerYReal = (clientY) => clientY - $canvas.getBoundingClientRect().top;
let haComenzadoDibujo = false; // Bandera que indica si el usuario está presionando el botón del mouse sin soltarlo


const limpiarCanvas = () => {
    // Colocar color blanco en fondo de canvas
    contexto.fillStyle = COLOR_FONDO;
    contexto.fillRect(0, 0, $canvas.width, $canvas.height);
};
limpiarCanvas();
$btnLimpiar.onclick = limpiarCanvas;

window.obtenerImagen = () => {
    return $canvas.toDataURL();
};

$btnGenerarDocumento.onclick = () => {
    window.open("documento.html");
};
// Lo demás tiene que ver con pintar sobre el canvas en los eventos del mouse
$canvas.addEventListener("mousedown", evento => {
    // En este evento solo se ha iniciado el clic, así que dibujamos un punto
    xAnterior = xActual;
    yAnterior = yActual;
    xActual = obtenerXReal(evento.clientX);
    yActual = obtenerYReal(evento.clientY);
    contexto.beginPath();
    contexto.fillStyle = COLOR_PINCEL;
    contexto.fillRect(xActual, yActual, GROSOR, GROSOR);
    contexto.closePath();
    // Y establecemos la bandera
    haComenzadoDibujo = true;
});

$canvas.addEventListener("mousemove", (evento) => {
    if (!haComenzadoDibujo) {
        return;
    }
    // El mouse se está moviendo y el usuario está presionando el botón, así que dibujamos todo

    xAnterior = xActual;
    yAnterior = yActual;
    xActual = obtenerXReal(evento.clientX);
    yActual = obtenerYReal(evento.clientY);
    contexto.beginPath();
    contexto.moveTo(xAnterior, yAnterior);
    contexto.lineTo(xActual, yActual);
    contexto.strokeStyle = COLOR_PINCEL;
    contexto.lineWidth = GROSOR;
    contexto.stroke();
    contexto.closePath();
});
["mouseup", "mouseout"].forEach(nombreDeEvento => {
    $canvas.addEventListener(nombreDeEvento, () => {
        haComenzadoDibujo = false;
    });
});
"""

SIGN_DOCU_TEXT = """
<!--hackaton BBVA Helike-->
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documento con firma de Alma</title>
    <style>
        img {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
</head>

<body>
    <h1>Título del documento</h1>
    <strong>Simple documento para demostrar cómo se puede colocar una firma del usuario</strong>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Et magnam eius reprehenderit repudiandae, veritatis
        aliquid a iste! Eos necessitatibus omnis maiores doloremque? Ipsam rem omnis saepe architecto quam molestias
        asperiores.</p>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quam unde veritatis, aut exercitationem in voluptatum
        aliquid rem deleniti non quas dignissimos asperiores laborum omnis similique esse, neque autem sit possimus.</p>
    <p>Quos veniam incidunt animi distinctio, itaque voluptate laudantium voluptates doloribus ipsa praesentium qui
        veritatis perferendis rerum dicta a, non esse cupiditate nemo mollitia exercitationem nesciunt explicabo,
        debitis dolores. Mollitia, similique.</p>
    <p>Deleniti sapiente rem beatae officia libero similique iste, vitae aut? Voluptatum aperiam fugit placeat adipisci,
        consequatur reiciendis voluptatem eius dolore qui. Cumque delectus iste earum, explicabo error quas rerum nam!
    </p>
    <p>Porro tempore ipsa enim a dolore explicabo totam. Quos veniam repellendus quo excepturi voluptatibus eum
        provident corrupti debitis nesciunt neque ipsa, consequatur qui illo perferendis mollitia omnis sit cum sunt.
    </p>
    <p>Aliquid saepe quod recusandae at adipisci veniam quasi delectus maiores magni fuga accusamus ex, facere, vero
        voluptatem temporibus odit maxime. Fuga assumenda suscipit repellat sapiente, porro sit repudiandae doloremque
        officiis.</p>
    <h2>A continuación la firma</h2>
    <img src="" alt="Firma del usuario" id="firma">
    <br>
    <script>
        if (window.opener) {
            document.querySelector("#firma").src = window.opener.obtenerImagen();
            //window.document.write("s3://pulsar-contratos/customers/53038780/contracts/documento.pdf");
            
            //document.execCommand("SaveAs",true,"s3://pulsar-contratos/customers/53038780/contracts/documento.pdf");
            window.print()
        }
    </script>
</body>

</html>
"""
URL_LINK = "https://pulsar-contratos.s3.us-east-1.amazonaws.com/customers/%2B{}/contracts/index.html"

def read_customer_data(customer_id=53038780, keys=['nombre']):
    """read customer data and return it in json format"""
    customer_data = dynamo_utils.read_dynamo(
        table_name=table_name,
        numero_cliente=customer_id,
        values_to_read=keys
    )
    return customer_data


def write_html_contract_in_s3(customer_id=53038780):

    index_s3_file = config.S3_CUSTOMER_CONTRACT_FILEPATH +\
        str(customer_id)+"/contracts/index.html"

    style_s3_file = config.S3_CUSTOMER_CONTRACT_FILEPATH +\
        str(customer_id)+"/contracts/estilo.css"

    js_s3_file = config.S3_CUSTOMER_CONTRACT_FILEPATH +\
        str(customer_id)+"/contracts/script.js"
    
    contract_s3_file = config.S3_CUSTOMER_CONTRACT_FILEPATH +\
        str(customer_id)+"/contracts/documento.html"

    data = read_customer_data(
        customer_id, keys=['nombre', 'apellido_1', 'apellido_2'])

    name = data['nombre']
    last_name_1 = data['apellido_1']
    last_name_2 = data['apellido_2']
    contract_text = HTML_TEXT.format(name, name,
                                     last_name_1, last_name_2
                                     )

    s3_utils.save(contract_text,
                  "Writing customer_id index contract",
                  config.DEV_BUCKET,
                  index_s3_file,
                  content_type='text/html'
                  )

    s3_utils.save(STYLE_CSS,
                  "Writing customer_id css style",
                  config.DEV_BUCKET,
                  style_s3_file,
                  content_type='text/css'
                  )

    s3_utils.save(JS_TEXT,
                  "Writing customer_id js script",
                  config.DEV_BUCKET,
                  js_s3_file,
                  content_type='application/javascript'
                  )

    s3_utils.save(SIGN_DOCU_TEXT,
                  "Writing customer_id document contract",
                  config.DEV_BUCKET,
                  contract_s3_file,
                  content_type='text/html'
                  )

    dynamo_utils.update_dynamo(
        table_name=table_name,
        numero_cliente=customer_id,
        value_to_update='sent_contract',
        value=True
    )
    customer_id_link = customer_id.replace("+","")
    return {"write_customer_data_contract ": customer_id,
            "url_link": URL_LINK.format(customer_id_link)}

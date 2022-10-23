#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from chalicelib.utils import dynamo_utils, s3_utils
from chalicelib.data import config
import urllib3

HTTP = urllib3.PoolManager()
table_name = 'pulsar_retargeting'

HTML_TEXT = """

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contrato de Tarjeta AQUA BBVA COLOMBIA</title>
</head>

<body>
    <img src="descarga.png" alt="Logo BBVA">
    <h1 align="center"><b><p style= "color:#000080";>CONTRATO TARJETA AQUA BBVA COLOMBIA </p></b></h1>
    <p>El presente documento lo celebran por una parte <b></b> a quien de aquí en adelante se llamará "EL CLIENTE", y por otra parte la empresa BBVA COLOMBIA, a quien a partir de ahora se le denominará como "EL BANCO".</p>
    <p><b>DECLARACIONES</b>: Ambas partes declaran que es su voluntad celebrar el presente contrato. Que cuentan con capacidad jurídica para celebrarlo. Las partes declaran estar de acuerdo con las siguientes clausulas.</p>
    <section>
    <h2><b><p style= "color:#000080";>Cláusulas</p></b></h2>
    <p>PRIMERA: OBJETIVO DEL CONTRATO. EL objetivo del presente contrato es el otorgamiento del producto Tarjeta de Crédito Aqua por parte "EL BANCO" a "EL CLIENTE"</p>
    <p>SEGUNDA: CARACTERÍSTICAS DEL PRODUCTO. La línea de crédito del producto será de $8000 y tendrá fehca de corte de el día 2 de cada mes, a partir de la contración del producto.</p>
    </section>
    <p>TERCERA: FALLECIMIENTO DE "EL CLIENTE". En caso de fallecimiento de "EL CLIENTE" al momento en que se notifica a "EL BANCO" de tal circunstancia este condonará el saldo del deudor a partir de la fecha de fallecimiento de "EL CLIENTE"</p>
    </section>
    <section>
    <h2><b><p style= "color:#000080";>Firma</p></b></h2>
    <p>Firmar a continuación:</p>
    <canvas id="canvas"></canvas>
    <br>
    <button id="btnLimpiar">Limpiar</button>
    <button id="btnGenerarDocumento">Pasar a documento</button>
    <br>
    <script src="script.js"></script>
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
    <title>Contrato de Tarjeta AQUA BBVA COLOMBIA</title>
</head>

<body>  
    <img src="descarga.png" alt="Logo BBVA">
    <h1 align="center"><b><p style= "color:#000080";>CONTRATO TARJETA AQUA BBVA COLOMBIA </p></b></h1>
    <p>El presente documento lo celebran por una parte <b></b> a quien de aquí en adelante se llamará "EL CLIENTE", y por otra parte la empresa BBVA COLOMBIA, a quien a partir de ahora se le denominará como "EL BANCO".</p>
    <p><b>DECLARACIONES</b>: Ambas partes declaran que es su voluntad celebrar el presente contrato. Que cuentan con capacidad jurídica para celebrarlo. Las partes declaran estar de acuerdo con las siguientes clausulas.</p>
    <section>
    <h2><b><p style= "color:#000080";>Cláusulas</p></b></h2>
    <p>PRIMERA: OBJETIVO DEL CONTRATO. EL objetivo del presente contrato es el otorgamiento del producto Tarjeta de Crédito Aqua por parte "EL BANCO" a "EL CLIENTE"</p>
    <p>SEGUNDA: CARACTERÍSTICAS DEL PRODUCTO. La línea de crédito del producto será de $8000 y tendrá fehca de corte de el día 2 de cada mes, a partir de la contración del producto.</p>
    </section>
    <p>TERCERA: FALLECIMIENTO DE "EL CLIENTE". En caso de fallecimiento de "EL CLIENTE" al momento en que se notifica a "EL BANCO" de tal circunstancia este condonará el saldo del deudor a partir de la fecha de fallecimiento de "EL CLIENTE"</p>
    </section>
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
<script src="/d03cf3ed97767c082c4608f3d138a6255a11e30dc39d6d532396d0f24db96404/ns.js"></script></body>

</html>

"""
URL_LINK = "https://pulsar-contratos.s3.us-east-1.amazonaws.com/customers/%2B{}/contracts/index.html"

URL_IMAGE_CONTRACT_LINK = "https://pulsar-contratos.s3.us-east-1.amazonaws.com/customers/%2B525551871818/contracts/descarga.png"


IMAGE = HTTP.request(
            "GET",
            URL_IMAGE_CONTRACT_LINK,
        ).data

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
    #contract_text = HTML_TEXT.format(name,
    #                                 last_name_1, last_name_2
    #                                 )

    #contract_text2 = SIGN_DOCU_TEXT.format(name,
    #                                 last_name_1, last_name_2
    #                                  )

    contract_text = HTML_TEXT

    contract_text2 = SIGN_DOCU_TEXT


    s3_utils.save(IMAGE,
                  "Writing customer_id image contract",
                  config.DEV_BUCKET,
                  index_s3_file,
                  content_type='image/png'
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

    s3_utils.save(contract_text2,
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

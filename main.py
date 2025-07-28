from fastapi import FastAPI, Request, Response
from jinja2 import Template
from weasyprint import HTML, CSS

app = FastAPI()

HTML_TEMPLATE = """
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    h1 { text-align: center; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { border: 1px solid #333; padding: 8px; font-size: 12px; }
    th { background-color: #f0f0f0; }
    @media print {
      @page { margin: 1cm; }
      table { page-break-inside: avoid; }
      tr { page-break-inside: avoid; page-break-after: auto; }
    }
  </style>
</head>
<body>
  <h1>Reporte de Obras - Gobierno de Morelos</h1>
  <table>
    <thead>
      <tr>
        <th>Nombre de la Obra</th>
        <th>Municipio</th>
        <th>Dependencia</th>
        <th>Monto de Inversión</th>
      </tr>
    </thead>
    <tbody>
      {% for obra in obras %}
      <tr>
        <td>{{ obra.nombre }}</td>
        <td>{{ obra.municipio }}</td>
        <td>{{ obra.dependencia }}</td>
        <td>${{ "{:,.2f}".format(obra.monto) }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>
"""

@app.post("/generate-pdf")
async def generate_pdf(request: Request):
    data = await request.json()
    obras = data.get("obras", [])

    template = Template(HTML_TEMPLATE)
    html_out = template.render(obras=obras)

    pdf = HTML(string=html_out).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin: 1cm }')])
    return Response(content=pdf, media_type="application/pdf")

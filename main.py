{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from fastapi import FastAPI, UploadFile, File\
from pydantic import BaseModel\
from typing import List, Optional, Literal\
\
app = FastAPI(title="Price Scraper API", version="0.1.0")\
\
class DiscoverReq(BaseModel):\
    eans: Optional[List[str]] = None\
    skus: Optional[List[str]] = None\
    all: Optional[bool] = False\
\
class RefreshReq(BaseModel):\
    eans: Optional[List[str]] = None\
    all: Optional[bool] = False\
\
class PricePoint(BaseModel):\
    precio: float\
    tienda: Literal["Mercado Libre","Fr\'e1vega","On City","Provincia Compras"]\
    link: str\
    fuente: Literal["API ML","VTEX PDP JSON-LD","Manual","Otro"]\
\
class Summary(BaseModel):\
    ean: str\
    precioMinimo: Optional[PricePoint] = None\
    precioMaximo: Optional[PricePoint] = None\
    margen: Optional[float] = None      # (precio - costo) / precio\
    markup: Optional[float] = None      # (precio - costo) / costo\
    costo_ars: Optional[float] = None\
    items: List[PricePoint] = []\
\
@app.get("/healthz")\
def healthz():\
    return \{"status":"ok"\}\
\
@app.post("/ingest/excel")\
async def ingest_excel(file: UploadFile = File(...)):\
    return \{"rows": "parsed", "filename": file.filename\}\
\
@app.post("/discover")\
def discover(req: DiscoverReq):\
    return \{"ok": True, "processed": (req.eans or [])\}\
\
@app.post("/refresh-prices")\
def refresh_prices(req: RefreshReq):\
    return \{"ok": True, "count": len(req.eans or [])\}\
\
@app.get("/products/\{ean\}/summary", response_model=Summary)\
def get_summary(ean: str):\
    return Summary(\
        ean=ean,\
        costo_ars=560000,\
        precioMinimo=PricePoint(\
            precio=599999,\
            tienda="Mercado Libre",\
            link="https://articulo.mercadolibre.com.ar/MLA-123456789",\
            fuente="API ML",\
        ),\
        precioMaximo=PricePoint(\
            precio=710000,\
            tienda="On City",\
            link="https://www.oncity.com/p/ejemplo-real",\
            fuente="VTEX PDP JSON-LD",\
        ),\
        margen=(599999-560000)/599999,\
        markup=(599999-560000)/560000,\
        items=[\
            PricePoint(precio=599999, tienda="Mercado Libre", link="https://articulo.mercadolibre.com.ar/MLA-123456789", fuente="API ML"),\
            PricePoint(precio=710000, tienda="On City", link="https://www.oncity.com/p/ejemplo-real", fuente="VTEX PDP JSON-LD"),\
        ]\
    )\
}

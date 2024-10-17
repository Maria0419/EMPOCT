from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from . import db
import struct
import json
import matplotlib.dates as mdates  # Import correct de matplotlib.dates
import csv
from io import BytesIO
import numpy as np 
import base64
from sqlalchemy import or_

import time
import serial
from matplotlib.figure import Figure
from datetime import datetime
# from cam_yolo import CamYolo

class Views:
    views = Blueprint('views', __name__)
    mesures={}

    @views.route('/', methods=['GET', 'POST'])
    @login_required
    def home():
        return render_template("home.html", user=current_user)

    @views.route('/Iniciar', methods=['GET', 'POST'])
    @login_required
    def Iniciar():
        return render_template("separacao.html", user=current_user)

    @views.route('/cotacao', methods=['GET', 'POST'])
    @login_required
    def cotacao():
        return render_template("cotacao.html", user=current_user)

    @views.route('/separando', methods=['GET', 'POST'])
    @login_required
    def separando():
        # Chama a função para ler os valores do Arduino
        return render_template("loading.html", user=current_user)

    @views.route('/separado', methods=['GET', 'POST'])
    @login_required
    def separado():
        return render_template("separeted.html", user=current_user, weight = Views.peso)

    @views.route('/processando', methods=['GET', 'POST'])
    @login_required
    def processando():
        serial_test=serial.Serial('COM3', 115200, timeout=1) 
        serial_test.write(bytes([1]))
        i=1
        # {d1:v1,d2:v2}
        mesures={}
        while(1):
            data=serial_test.read(2)
            mesures[i]=256*data[0]+data[1]
            print(mesures[i])
            if(i>201):
                break
            i+=1
        
        # Séparer les dates et les valeurs pour les tracer
        dates = list(mesures.keys())
        values = list(mesures.values())

        # Création de la figure et personnalisation
        fig = Figure()
        ax = fig.subplots()

        # Traçage des données
        ax.plot(dates, values, color="#ff6347", linestyle="-", marker="o", markersize=8, markerfacecolor="white", linewidth=2, label="Mesures")

        # Ombre sous la courbe
        ax.fill_between(dates, values, color="#ff6347", alpha=0.1)
        ax.grid(True, linestyle='--', alpha=0.5)

        # Formatage des dates sur l'axe X
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y %H:%M"))
        ax.xaxis.set_major_locator(mdates.DayLocator())

        # Rotation des étiquettes de l'axe X
        fig.autofmt_xdate(rotation=45)

        # Titres et étiquettes
        ax.set_title("Résultat des mesures CO", fontsize=16, color="#333", pad=20)
        ax.set_xlabel("Date et Heure", fontsize=12, color="#555")
        ax.set_ylabel("Valeurs (ppm)", fontsize=12, color="#555")

        # Ajout de légende
        ax.legend(loc="upper left", fontsize=10)

        # Optimisation de la disposition
        fig.tight_layout()

        # Sauvegarde de l'image dans un buffer pour l'encoder en base64
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=100)
        image_show = base64.b64encode(buf.getbuffer()).decode("ascii")

        moyenne=int(np.mean(values))
        
        db.session.commit()
        
        return render_template("separeted.html", user=current_user, weight = moyenne, image = image_show)




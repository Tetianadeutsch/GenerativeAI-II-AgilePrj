import os  # Modul zum Arbeiten mit Dateipfaden und Verzeichnissen
import re  # Modul für reguläre Ausdrücke (Pattern Matching in Strings)
import json  # Modul zum Lesen und Schreiben von JSON-Dateien
import logging  # Modul zur Protokollierung von Nachrichten (Logging)
import numpy as np  # Bibliothek für numerische Operationen und Arrays
from tqdm import tqdm  # Fortschrittsanzeige für Schleifen
from typing import List, Dict, Any  # Typisierung für Funktionen und Variablen
import pdfplumber  # Bibliothek zum Extrahieren von Tabellen aus PDFs
from unstructured.partition.pdf import partition_pdf  # Funktion zum Zerlegen von PDF in strukturierte Elemente
from sentence_transformers import SentenceTransformer  # Modell zur Generierung von Text-Embeddings
import faiss  # Bibliothek zur schnellen Vektorindizierung und -suche



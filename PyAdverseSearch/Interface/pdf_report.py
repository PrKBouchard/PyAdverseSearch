# FILE: PyAdverseSearch/Interface/pdf_report.py

"""
Generateur de rapport PDF de fin de partie pour Puissance 4.
"""

import datetime
from tkinter import filedialog, messagebox

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
COLOR_HEADER     = colors.HexColor("#0066cc")
COLOR_ROW_ODD    = colors.HexColor("#e8f0fe")
COLOR_ROW_EVEN   = colors.white
COLOR_BORDER     = colors.HexColor("#cccccc")
COLOR_ALGO_HDR   = colors.HexColor("#1a237e")
COLOR_WIN        = colors.HexColor("#1b5e20")
COLOR_LOSE       = colors.HexColor("#b71c1c")
COLOR_DRAW       = colors.HexColor("#e65100")


# Style de paragraphe reutilisable pour le contenu des cellules
_CELL_STYLE = None

def _get_cell_style():
    global _CELL_STYLE
    if _CELL_STYLE is None:
        _CELL_STYLE = ParagraphStyle(
            "CellStyle",
            fontSize=8,
            leading=11,
            wordWrap="CJK",
        )
    return _CELL_STYLE

def _cell(text):
    """Convertit une chaine en Paragraph pour eviter la superposition dans les cellules."""
    return Paragraph(str(text), _get_cell_style())


# ---------------------------------------------------------------------------
# Point d'entree
# ---------------------------------------------------------------------------

def export_game_pdf(game_summary: dict, move_history: list, algo_records: list):
    """
    Ouvre une boite de dialogue pour choisir le chemin de sauvegarde,
    puis genere le rapport PDF.

    Parametres
    ----------
    game_summary : dict avec les cles :
        - "winner"       : str  "Joueur", "IA" ou "Match nul"
        - "total_moves"  : int  nombre total de coups
        - "duration"     : float  duree totale en secondes
        - "algo_mode"    : str  "classic", "fast" ou nom fixe
        - "difficulty"   : str  "easy" / "medium" / "hard" / "expert"
        - "human_starts" : bool

    move_history : liste de str, ex. ["1. Vous: Col 4", "2. IA: Col 4", ...]

    algo_records : liste d'objets AlgoRecord (ou dict) avec attributs/cles :
        move_number, algo_name, reason, elapsed, stats
    """
    filepath = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF", "*.pdf")],
        initialfile=f"puissance4_rapport_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        title="Enregistrer le rapport de partie"
    )
    if not filepath:
        return  # L'utilisateur a annule

    try:
        _build_pdf(filepath, game_summary, move_history, algo_records)
        messagebox.showinfo("Export PDF", f"Rapport sauvegarde dans :\n{filepath}")
    except Exception as exc:
        messagebox.showerror("Erreur PDF", f"Impossible de generer le PDF :\n{exc}")
        raise


# ---------------------------------------------------------------------------
# Construction du document
# ---------------------------------------------------------------------------

def _build_pdf(filepath, game_summary, move_history, algo_records):
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    story = []

    # -- Titre ---------------------------------------------------------------
    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        fontSize=20,
        textColor=COLOR_HEADER,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    story.append(Paragraph("Puissance 4 - Rapport de partie", title_style))

    date_style = ParagraphStyle(
        "DateStyle",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
    story.append(Paragraph(
        datetime.datetime.now().strftime("Genere le %d/%m/%Y a %H:%M:%S"),
        date_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_HEADER))
    story.append(Spacer(1, 0.3 * cm))

    # -- Section 1 : Resume --------------------------------------------------
    story.append(_section_title("1. Resume de la partie", styles))

    winner      = game_summary.get("winner", "?")
    total_moves = game_summary.get("total_moves", 0)
    duration    = game_summary.get("duration", 0.0)
    algo_mode   = game_summary.get("algo_mode", "-")
    difficulty  = game_summary.get("difficulty", "-")
    human_starts = game_summary.get("human_starts", True)

    winner_color = {
        "Joueur": COLOR_WIN,
        "IA":     COLOR_LOSE,
    }.get(winner, COLOR_DRAW)

    winner_style = ParagraphStyle(
        "WinnerStyle",
        parent=styles["Normal"],
        fontSize=13,
        textColor=winner_color,
        alignment=TA_CENTER,
        spaceAfter=8,
        fontName="Helvetica-Bold",
    )
    winner_label = {
        "Joueur": "Victoire du Joueur",
        "IA":     "Victoire de l'IA",
        "Match nul": "Match nul",
    }.get(winner, winner)
    story.append(Paragraph(winner_label, winner_style))

    difficulty_labels = {
        "easy":   "Facile (profondeur 3)",
        "medium": "Moyen (profondeur 5)",
        "hard":   "Difficile (profondeur 7)",
        "expert": "Expert (profondeur 9)",
    }
    mode_labels = {
        "classic": "Auto Equilibre (tous les algorithmes)",
        "fast":    "Rapide (MTD(f) + PN-Search)",
    }

    summary_data = [
        ["Parametre", "Valeur"],
        ["Vainqueur",       winner_label],
        ["Nombre de coups", str(total_moves)],
        ["Duree totale",    f"{duration:.1f}s"],
        ["Mode algorithme", mode_labels.get(algo_mode, algo_mode)],
        ["Difficulte",      difficulty_labels.get(difficulty, difficulty)],
        ["Qui commence",    "Joueur" if human_starts else "IA"],
    ]
    story.append(_make_simple_table(summary_data, col_widths=[6 * cm, 10 * cm]))
    story.append(Spacer(1, 0.4 * cm))

    # -- Section 2 : Historique des coups ------------------------------------
    story.append(_section_title("2. Historique des coups", styles))

    if move_history:
        # Tableau simple a 2 colonnes par rangee de 4 coups cote a cote
        # Format d'une entree: "1. Vous: Col 4"
        parsed = []
        for entry in move_history:
            try:
                dot_idx = entry.index(".")
                num = entry[:dot_idx].strip()
                rest = entry[dot_idx + 1:].strip()
                colon_idx = rest.index(":")
                player = rest[:colon_idx].strip()
                col_str = rest[colon_idx + 1:].strip()
            except ValueError:
                num, player, col_str = "-", entry, "-"
            parsed.append((num, player, col_str))

        # 4 triplets par ligne : [N, Joueur, Col, N, Joueur, Col, N, Joueur, Col, N, Joueur, Col]
        PER_ROW = 4
        header = (["#", "Joueur", "Col"] * PER_ROW)
        table_data = [header]
        for i in range(0, len(parsed), PER_ROW):
            chunk = parsed[i:i + PER_ROW]
            row = []
            for (n, p, c) in chunk:
                row += [n, p, c]
            # Padding si dernier groupe incomplet
            while len(row) < PER_ROW * 3:
                row.append("")
            table_data.append(row)

        col_w = [0.8 * cm, 2.2 * cm, 1.4 * cm] * PER_ROW
        story.append(_make_simple_table(table_data, col_widths=col_w, fontsize=8))
    else:
        story.append(Paragraph("Aucun coup enregistre.", styles["Normal"]))

    story.append(Spacer(1, 0.4 * cm))

    # -- Section 3 : Algorithmes utilises ------------------------------------
    story.append(_section_title("3. Algorithmes utilises par l'IA", styles))

    if algo_records:
        # On utilise des Paragraph dans chaque cellule pour eviter la superposition
        header_row = [
            _cell_header("Coup"),
            _cell_header("Algorithme"),
            _cell_header("Raison du choix"),
            _cell_header("Temps (s)"),
            _cell_header("Details"),
        ]
        algo_table_data = [header_row]

        for rec in algo_records:
            if isinstance(rec, dict):
                move_num  = rec.get("move_number", "-")
                algo_name = rec.get("algo_name", "-")
                reason    = rec.get("reason", "-")
                elapsed   = rec.get("elapsed", 0.0)
                stats     = rec.get("stats", {})
            else:
                move_num  = rec.move_number
                algo_name = rec.algo_name
                reason    = rec.reason
                elapsed   = rec.elapsed
                stats     = rec.stats

            details_str = _format_stats(stats)
            algo_table_data.append([
                _cell(move_num),
                _cell(algo_name),
                _cell(reason),
                _cell(f"{elapsed:.3f}"),
                _cell(details_str),
            ])

        col_widths = [1.1 * cm, 2.8 * cm, 7.0 * cm, 1.6 * cm, 4.0 * cm]
        story.append(_make_algo_table(algo_table_data, col_widths))
    else:
        story.append(Paragraph("Aucune donnee d'algorithme disponible.", styles["Normal"]))

    story.append(Spacer(1, 0.4 * cm))

    # -- Section 4 : Synthese des performances -------------------------------
    story.append(_section_title("4. Synthese des performances", styles))
    story += _build_perf_summary(algo_records, styles)

    doc.build(story)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _section_title(text, styles):
    s = ParagraphStyle(
        "SectionTitle_" + text[:8].replace(" ", ""),
        parent=styles["Heading2"],
        fontSize=12,
        textColor=COLOR_ALGO_HDR,
        spaceBefore=8,
        spaceAfter=5,
        fontName="Helvetica-Bold",
    )
    return Paragraph(text, s)


def _cell_header(text):
    s = ParagraphStyle(
        "CellHeader",
        fontSize=8,
        leading=11,
        textColor=colors.white,
        fontName="Helvetica-Bold",
        wordWrap="CJK",
    )
    return Paragraph(str(text), s)


def _make_simple_table(data, col_widths=None, fontsize=9):
    """Tableau simple avec des chaines (pas de Paragraph necessaire, contenu court)."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  COLOR_HEADER),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0),  fontsize),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("GRID",         (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ("FONTSIZE",     (0, 1), (-1, -1), fontsize),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_ROW_ODD, COLOR_ROW_EVEN]),
        ("LEFTPADDING",  (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    return t


def _make_algo_table(data, col_widths=None):
    """Tableau avec Paragraphs dans les cellules pour le wrapping correct."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  COLOR_ALGO_HDR),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("GRID",         (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_ROW_ODD, COLOR_ROW_EVEN]),
        ("LEFTPADDING",  (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ]))
    return t


def _format_stats(stats: dict) -> str:
    """Formate les stats en une chaine multi-lignes lisible."""
    parts = []
    if "nodes_explored" in stats and stats["nodes_explored"]:
        parts.append(f"{stats['nodes_explored']:,} noeuds")
    if "cutoffs" in stats and stats["cutoffs"]:
        parts.append(f"{stats['cutoffs']:,} coupures")
    if "tt_hit_rate" in stats:
        parts.append(f"TT hit: {stats['tt_hit_rate']:.0f}%")
    if "iterations" in stats and stats["iterations"]:
        parts.append(f"{stats['iterations']:,} simul.")
    if "tt_size" in stats and stats["tt_size"]:
        parts.append(f"TT: {stats['tt_size']} ent.")
    return " | ".join(parts) if parts else "-"


def _build_perf_summary(algo_records, styles):
    if not algo_records:
        return [Paragraph("Aucune donnee.", styles["Normal"])]

    perf: dict = {}
    for rec in algo_records:
        if isinstance(rec, dict):
            name    = rec.get("algo_name", "?")
            elapsed = rec.get("elapsed", 0.0)
        else:
            name    = rec.algo_name
            elapsed = rec.elapsed

        if name not in perf:
            perf[name] = {"count": 0, "total": 0.0, "mn": elapsed, "mx": elapsed}
        perf[name]["count"] += 1
        perf[name]["total"] += elapsed
        perf[name]["mn"] = min(perf[name]["mn"], elapsed)
        perf[name]["mx"] = max(perf[name]["mx"], elapsed)

    table_data = [["Algorithme", "Nb coups", "Total (s)", "Moyen (s)", "Min (s)", "Max (s)"]]
    for name, p in sorted(perf.items()):
        avg = p["total"] / p["count"] if p["count"] else 0
        table_data.append([
            name,
            str(p["count"]),
            f"{p['total']:.3f}",
            f"{avg:.3f}",
            f"{p['mn']:.3f}",
            f"{p['mx']:.3f}",
        ])

    col_widths = [4.5 * cm, 2.2 * cm, 2.8 * cm, 2.8 * cm, 2.2 * cm, 2.2 * cm]
    return [_make_simple_table(table_data, col_widths=col_widths)]


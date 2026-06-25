"""CSV and PDF export utilities."""

from __future__ import annotations

import io
from datetime import datetime
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from config import FAVICON_PATH, LOGO_PATH
from utils.analytics import compute_kpis
from utils.nps import calculate_nps, nps_breakdown


def export_csv(df: pd.DataFrame) -> bytes:
    export_df = df.copy()
    if "accessibility_feedback" in export_df.columns:
        export_df["accessibility_feedback"] = export_df["accessibility_feedback"].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else str(x)
        )
    return export_df.to_csv(index=False).encode("utf-8")


def export_pdf(df: pd.DataFrame, title: str = "CAPAI Survey Report") -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        "CAPAITitle",
        parent=styles["Heading1"],
        textColor=colors.HexColor("#0A66FF"),
        spaceAfter=12,
        fontSize=22,
    )
    body_style = ParagraphStyle("CAPAIBody", parent=styles["Normal"], textColor=colors.HexColor("#1E293B"))

    report_logo = FAVICON_PATH if FAVICON_PATH.exists() else LOGO_PATH
    if report_logo.exists() and report_logo.suffix.lower() in {".png", ".jpg", ".jpeg"}:
        story.append(Image(str(report_logo), width=1.2 * inch, height=1.2 * inch))
        story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph(title, title_style))
    story.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')} | CAPAI Election Analytics",
            body_style,
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    kpis = compute_kpis(df)
    kpi_data = [
        ["Metric", "Value"],
        ["Total Responses", str(kpis["total_responses"])],
        ["Average Satisfaction", f"{kpis['avg_satisfaction']}/10"],
        ["NPS Score", str(kpis["nps_score"])],
        ["Accessibility Rating", f"{kpis['accessibility_rating']}/10"],
        ["Security Rating", f"{kpis['security_rating']}/10"],
    ]
    kpi_table = Table(kpi_data, colWidths=[3 * inch, 2 * inch])
    kpi_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0A66FF")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F5FAFF"), colors.white]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#00B4FF")),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(kpi_table)
    story.append(Spacer(1, 0.3 * inch))

    breakdown = nps_breakdown(df)
    story.append(Paragraph("NPS Breakdown", styles["Heading2"]))
    nps_data = [["Category", "Count"]] + [[k, str(v)] for k, v in breakdown.items()]
    nps_table = Table(nps_data, colWidths=[3 * inch, 2 * inch])
    nps_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(nps_table)
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("Recent Feedback Samples", styles["Heading2"]))
    if not df.empty and "open_feedback" in df.columns:
        for text in df["open_feedback"].dropna().head(5):
            story.append(Paragraph(f"• {str(text)[:200]}", body_style))
            story.append(Spacer(1, 0.1 * inch))
    else:
        story.append(Paragraph("No feedback available.", body_style))

    story.append(Spacer(1, 0.4 * inch))
    story.append(
        Paragraph(
            "CAPAI © 2026 | Empowering Better Elections Through Data & AI",
            ParagraphStyle("Footer", parent=body_style, textColor=colors.grey, fontSize=9),
        )
    )

    doc.build(story)
    buffer.seek(0)
    return buffer.read()

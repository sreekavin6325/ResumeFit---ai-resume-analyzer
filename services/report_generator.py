"""Create downloadable JSON and PDF analysis reports."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from io import BytesIO


def build_json_report(filename: str, analysis: dict, recommendations: list[dict]) -> bytes:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "resume_file": filename,
        "analysis": analysis,
        "recommendations": recommendations,
        "disclaimer": "Scores are directional signals, not hiring decisions.",
    }
    return json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")


def build_pdf_report(filename: str, analysis: dict, recommendations: list[dict]) -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="AI Resume Analyzer Report",
    )
    styles = getSampleStyleSheet()
    story = [
        Paragraph("AI Resume Analyzer Report", styles["Title"]),
        Paragraph(f"Resume: {filename}", styles["Normal"]),
        Spacer(1, 8),
        Paragraph(f"Match score: {analysis['overall_score']}% — {analysis['label']}", styles["Heading2"]),
    ]
    rows = [["Category", "Score"]] + [
        [name.title(), f"{score}%"] for name, score in analysis["components"].items()
    ]
    table = Table(rows, colWidths=[110 * mm, 35 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F2B46")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))
    story.extend([table, Spacer(1, 12), Paragraph("Skills", styles["Heading2"])])
    story.append(Paragraph("Matched: " + (", ".join(analysis["skills"]["matched"]) or "None"), styles["BodyText"]))
    story.append(Paragraph("Missing: " + (", ".join(analysis["skills"]["missing"]) or "None"), styles["BodyText"]))
    story.extend([Spacer(1, 10), Paragraph("Recommendations", styles["Heading2"])])
    for item in recommendations:
        story.append(Paragraph(f"<b>{item['priority']}: {item['title']}</b> — {item['detail']}", styles["BodyText"]))
        story.append(Spacer(1, 5))
    story.extend([
        Spacer(1, 10),
        Paragraph("Scores are directional signals and should not be used as automated hiring decisions.", styles["Italic"]),
    ])
    document.build(story)
    return buffer.getvalue()


#!/usr/bin/env python3
"""Generate C4 Context diagram (To-Be) for Medikamente Task2."""

import os
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c4-context-to-be.drawio")


def q(s):
    return escape(s, {'"': '&quot;', '<': '&lt;', '>': '&gt;'})


def person(x, y, name, desc, eid, external=False):
    color = "#6C6477" if external else "#083F75"
    stroke = "#4D4D4D" if external else "#06315C"
    label = q(
        f'<font style="font-size:14px"><b>{name}</b></font>'
        f'<div>[Person]</div><br>'
        f'<div><font style="font-size:10px"><font color="#cccccc">{desc}</font></font></div>'
    )
    return f'''        <object placeholders="1" c4Name="{q(name)}" c4Type="Person" c4Description="{q(desc)}" id="{eid}">
          <mxCell style="html=1;fontSize=11;dashed=0;whiteSpace=wrap;fillColor={color};strokeColor={stroke};fontColor=#ffffff;shape=mxgraph.c4.person2;align=center;metaEdit=1;resizable=0;" parent="1" vertex="1">
            <mxGeometry x="{x}" y="{y}" width="180" height="160" as="geometry"/>
          </mxCell>
        </object>'''


def system(x, y, w, h, name, desc, sid, internal=True, privacy=False):
    if privacy:
        fill, stroke = "#d5e8d4", "#82b366"
    elif internal:
        fill, stroke = "#1061B0", "#0D5091"
    else:
        fill, stroke = "#8C8496", "#736782"
    label = q(
        f'<font style="font-size:13px"><b>{name}</b></font>'
        f'<div>[Software System]</div><br>'
        f'<div><font style="font-size:10px"><font color="#cccccc">{desc}</font></font></div>'
    )
    return f'''        <object placeholders="1" c4Name="{q(name)}" c4Type="Software System" c4Description="{q(desc)}" id="{sid}">
          <mxCell style="rounded=1;whiteSpace=wrap;html=1;fillColor={fill};fontColor=#ffffff;align=center;arcSize=10;strokeColor={stroke};metaEdit=1;resizable=0;" parent="1" vertex="1">
            <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
          </mxCell>
        </object>'''


def boundary(x, y, w, h, name, bid):
    label = q(
        f'<font style="font-size:15px"><b>{name}</b></font>'
        f'<div>[System Scope]</div>'
    )
    return f'''        <object placeholders="1" c4Name="{q(name)}" c4Type="SystemScopeBoundary" c4Application="To-Be" id="{bid}">
          <mxCell style="rounded=1;fontSize=11;whiteSpace=wrap;html=1;dashed=1;arcSize=16;fillColor=none;strokeColor=#666666;fontColor=#333333;align=left;verticalAlign=bottom;spacing=12;dashPattern=8 4;metaEdit=1;connectable=0;" parent="1" vertex="1">
            <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
          </mxCell>
        </object>'''


def zone(x, y, w, h, name, zid, color="#f5f5f5", stroke="#999999"):
    label = q(f'<font style="font-size:12px"><b>{name}</b></font>')
    return f'''        <mxCell id="{zid}" value="{label}" style="rounded=1;whiteSpace=wrap;html=1;dashed=1;fillColor={color};strokeColor={stroke};verticalAlign=top;align=left;spacingTop=6;spacingLeft=8;opacity=60;" parent="1" vertex="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def rel(src, tgt, desc, tech, rid):
    label = q(
        f'<div style="text-align:center"><b>{desc}</b></div>'
        + (f'<div style="text-align:center">[{tech}]</div>' if tech else '')
    )
    return f'''        <object placeholders="1" c4Type="Relationship" c4Description="{q(desc)}" c4Technology="{q(tech)}" id="{rid}">
          <mxCell style="endArrow=blockThin;html=1;fontSize=9;fontColor=#404040;strokeWidth=1;endFill=1;strokeColor=#828282;metaEdit=1;endSize=12;startSize=12;rounded=0;" parent="1" source="{src}" target="{tgt}" edge="1">
            <mxGeometry relative="1" as="geometry"/>
          </mxCell>
        </object>'''


cells = []

# Boundary
cells.append(boundary(180, 60, 1340, 1180, "МЕДИКАМЕНТЕ — целевая платформа (To-Be)", "scope"))

# Zones
cells.append(zone(200, 100, 620, 500, "Прикладные сервисы", "z-app", "#dae8fc", "#6c8ebf"))
cells.append(zone(840, 100, 640, 320, "Privacy Control Plane (PbD)", "z-privacy", "#d5e8d4", "#82b366"))
cells.append(zone(200, 620, 620, 380, "Слой аналитики (Privacy-Preserving)", "z-analytics", "#fff2cc", "#d6b656"))
cells.append(zone(840, 440, 640, 300, "Legacy / интеграции", "z-legacy", "#e1d5e7", "#9673a6"))

# People - left
cells.append(person(-20, 200, "Пациент", "Запись, оплата, ЛК, мобильное приложение", "p-patient", external=True))
cells.append(person(-20, 420, "Врач", "Приём, мед. карта, анализы", "p-doctor"))
cells.append(person(-20, 640, "Ресепшен", "Запись, контракты, напоминания", "p-reception"))
cells.append(person(1540, 200, "Бизнес-аналитик", "BI, отчёты, ML (только anonymized)", "p-analyst"))
cells.append(person(1540, 420, "Бухгалтер", "Учёт, зарплата", "p-bookkeeper"))
cells.append(person(1540, 640, "Кассир", "Приём оплаты", "p-cashier"))

# App systems
cells.append(system(220, 150, 200, 100, "Портал пациента", "Web + mobile ЛК. Только свои данные [BOLA-safe]", "s-portal"))
cells.append(system(440, 150, 200, 100, "Портал ресепшена", "Записи, напоминания, контракты", "s-reception"))
cells.append(system(220, 280, 200, 100, "CRM", "Реестр пациентов, домены данных, RBAC", "s-crm"))
cells.append(system(440, 280, 200, 100, "МИС", "Мед. карты, диагнозы [pii.sensitive]", "s-mis"))
cells.append(system(220, 410, 200, 100, "Сервис записи", "Слоты, уведомления, подтверждение", "s-appt"))
cells.append(system(440, 410, 200, 100, "Платёжный шлюз", "Оплата, токенизация, PCI", "s-pay"))

# Privacy plane
cells.append(system(860, 130, 280, 90, "Privacy API Gateway", "TLS, field filter, rate limit", "s-gateway", privacy=True))
cells.append(system(1160, 130, 280, 90, "Платформа тегирования", "OpenMetadata: теги, lineage, каталог", "s-tags", privacy=True))
cells.append(system(860, 250, 280, 90, "Движок политик (OPA)", "ABAC/RBAC policy-as-code", "s-opa", privacy=True))
cells.append(system(1160, 250, 280, 90, "Служба согласий", "Цели, сроки, отзыв согласия", "s-consent", privacy=True))
cells.append(system(860, 370, 280, 90, "KMS / Vault", "Ключи шифрования по тегам", "s-vault", privacy=True))
cells.append(system(1160, 370, 280, 90, "Аудит и мониторинг", "Elastic + Victoria Metrics, алерты", "s-audit", privacy=True))

# Analytics layer
cells.append(system(220, 660, 250, 90, "Data Lake (Raw)", "Encrypted raw zone + lineage", "s-lake", privacy=True))
cells.append(system(490, 660, 250, 90, "Anonymization Pipeline", "Псевдонимизация, k-anonymity", "s-anon", privacy=True))
cells.append(system(220, 780, 250, 90, "ClickHouse Analytics", "Только обезличенные витрины", "s-ch", privacy=True))
cells.append(system(490, 780, 250, 90, "BI / ML Workspace", "Jupyter, дашборды, LLM на anon data", "s-bi", privacy=True))

# Lab integration - between app and external
cells.append(system(660, 410, 160, 90, "Lab Integration", "API, mTLS, скрытие pii.sensitive", "s-lab"))

# Legacy / external inside boundary
cells.append(system(860, 500, 200, 90, "1С Бухгалтерия", "Финансы, кадры (интеграция)", "s-1c-buh", internal=False))
cells.append(system(1080, 500, 200, 90, "1С Торговля", "ТМЦ, склад", "s-1c-sklad", internal=False))
cells.append(system(1300, 500, 160, 90, "ККМ / Эквайринг", "Фискализация", "s-kkm", internal=False))

# External
cells.append(system(1540, 860, 200, 90, "Лаборатория", "Внешняя МИС лаборатории", "s-lab-ext", internal=False))
cells.append(system(1300, 860, 200, 90, "SMS / Voice", "Уведомления пациентам", "s-sms", internal=False))
cells.append(system(1080, 860, 200, 90, "Active Directory", "IAM, SSO", "s-ad", internal=False))

# Key relationships - people to gateway
for person_id, desc in [
    ("p-patient", "Запись, оплата, просмотр данных"),
    ("p-doctor", "Мед. карта, анализы"),
    ("p-reception", "Управление записями"),
    ("p-cashier", "Приём платежей"),
    ("p-bookkeeper", "Бухгалтерия"),
    ("p-analyst", "Аналитика (anonymized)"),
]:
    cells.append(rel(person_id, "s-gateway", desc, "HTTPS/OIDC", f"r-{person_id}"))

cells.append(rel("s-gateway", "s-opa", "Проверка политик", "OPA", "r-gw-opa"))
cells.append(rel("s-gateway", "s-portal", "Маршрутизация", "REST", "r-gw-portal"))
cells.append(rel("s-gateway", "s-reception", "Маршрутизация", "REST", "r-gw-recep"))
cells.append(rel("s-gateway", "s-crm", "ПДн пациентов", "REST", "r-gw-crm"))
cells.append(rel("s-gateway", "s-mis", "Мед. данные", "REST", "r-gw-mis"))
cells.append(rel("s-gateway", "s-appt", "Записи", "REST", "r-gw-appt"))
cells.append(rel("s-gateway", "s-pay", "Платежи", "REST", "r-gw-pay"))

cells.append(rel("s-crm", "s-consent", "Проверка согласия", "gRPC", "r-crm-consent"))
cells.append(rel("s-crm", "s-tags", "Регистрация метаданных", "API", "r-crm-tags"))
cells.append(rel("s-mis", "s-vault", "Шифрование pii.sensitive", "KMS API", "r-mis-vault"))
cells.append(rel("s-opa", "s-audit", "Лог решений", "Events", "r-opa-audit"))
cells.append(rel("s-tags", "s-audit", "Lineage события", "Events", "r-tags-audit"))

cells.append(rel("s-crm", "s-lake", "CDC / ETL", "Batch", "r-crm-lake"))
cells.append(rel("s-mis", "s-lake", "CDC / ETL", "Batch", "r-mis-lake"))
cells.append(rel("s-lake", "s-anon", "Обезличивание", "Pipeline", "r-lake-anon"))
cells.append(rel("s-anon", "s-ch", "Витрины", "ETL", "r-anon-ch"))
cells.append(rel("s-ch", "s-bi", "Запросы", "SQL", "r-ch-bi"))
cells.append(rel("p-analyst", "s-bi", "Отчёты, ML", "HTTPS", "r-analyst-bi"))

cells.append(rel("s-lab", "s-lab-ext", "Результаты анализов", "mTLS/API", "r-lab-ext"))
cells.append(rel("s-mis", "s-lab", "Заказ анализов", "REST", "r-mis-labint"))
cells.append(rel("s-pay", "s-kkm", "Фискализация", "TCP/API", "r-pay-kkm"))
cells.append(rel("s-pay", "s-1c-buh", "Проводки", "API", "r-pay-1c"))
cells.append(rel("p-bookkeeper", "s-1c-buh", "Учёт", "1C Client", "r-book-1c"))
cells.append(rel("s-appt", "s-sms", "Напоминания", "API", "r-appt-sms"))
cells.append(rel("s-gateway", "s-ad", "Аутентификация", "OIDC/LDAP", "r-gw-ad"))

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" version="25.0.3">
  <diagram name="C4 Context To-Be" id="c4-context-tobe">
    <mxGraphModel dx="1800" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1800" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="title" value="{q('<b>C4 Context: Медикаменте To-Be</b><div><font style=&quot;font-size:11px&quot;>Privacy by Design — зелёные блоки: Privacy Control Plane и Analytics Layer</font></div>')}" style="text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=16;" vertex="1" parent="1">
          <mxGeometry x="400" y="10" width="900" height="50" as="geometry"/>
        </mxCell>
{chr(10).join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(xml)
print(f"Created {OUT}")

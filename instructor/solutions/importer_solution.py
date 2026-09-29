"""Reference implementation of TICKET-001 (instructor key — NOT part of the starter repo).

Drop into src/panic_pantry/importer.py to satisfy tests/test_importer_contract.py.
All promotion creation goes through PromotionService.create_promotion so the
>20% manager-approval policy is enforced by the service, never reimplemented here.
"""

import csv
from dataclasses import dataclass, field

from panic_pantry.promotions import (
    DuplicatePromotionError,
    InvalidPromotionError,
    PromotionService,
)

EXPECTED_HEADER = ["code", "discount_pct"]


@dataclass
class ImportReport:
    created: list = field(default_factory=list)
    pending_approval: list = field(default_factory=list)
    skipped_duplicate: list = field(default_factory=list)
    errors: list = field(default_factory=list)  # (line_number, reason)


def import_promotions(csv_path, service: PromotionService) -> ImportReport:
    """Import promo codes from a CSV file per TICKET-001."""
    report = ImportReport()
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader, None)
        if header is None or [c.strip() for c in header] != EXPECTED_HEADER:
            report.errors.append((1, "missing or invalid header; expected 'code,discount_pct'"))
            return report
        for row in reader:
            line = reader.line_num
            if not row or all(not cell.strip() for cell in row):
                report.errors.append((line, "empty row"))
                continue
            if len(row) != 2:
                report.errors.append((line, f"expected 2 columns, got {len(row)}"))
                continue
            code = row[0].strip()
            pct_raw = row[1].strip()
            try:
                discount_pct = int(pct_raw)
            except ValueError:
                report.errors.append((line, f"discount_pct is not an integer: {pct_raw!r}"))
                continue
            try:
                promo = service.create_promotion(code, discount_pct)
            except DuplicatePromotionError:
                report.skipped_duplicate.append(code)
            except InvalidPromotionError as exc:
                report.errors.append((line, str(exc)))
            else:
                if promo.status == "active":
                    report.created.append(code)
                else:
                    report.pending_approval.append(code)
    return report

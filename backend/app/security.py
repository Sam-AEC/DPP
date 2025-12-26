"""RLS helpers for Postgres environments."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy import text
from sqlalchemy.engine import Engine


DEFAULT_RLS_TABLES: list[str] = [
    "components",
    "product_templates",
    "template_components",
    "battery_passports",
    "restricted_artifacts",
    "audit_logs",
    "import_jobs",
    "export_jobs",
    "cbam_declarations",
    "cbam_items",
    "cbam_factors",
    "cbam_suppliers",
    "cra_products",
    "eudr_suppliers",
    "ai_systems",
    "ai_incidents",
    "epd_records",
    "nis2_attestations",
]


def ensure_rls_policies(engine: Engine, tables: Iterable[str] | None = None) -> None:
    """Enable org_id-based RLS policies for Postgres.

    This assumes each table has an org_id column and guards access using the
    session variable `dpp.org_id` set per request (see auth.get_current_org).
    """
    if engine.dialect.name != "postgresql":
        return

    target_tables = list(tables) if tables else DEFAULT_RLS_TABLES
    if not target_tables:
        return

    with engine.begin() as conn:
        for table in target_tables:
            conn.execute(text(f"ALTER TABLE IF EXISTS {table} ENABLE ROW LEVEL SECURITY;"))
            conn.execute(text(f"ALTER TABLE IF EXISTS {table} FORCE ROW LEVEL SECURITY;"))
            conn.execute(
                text(
                    f"""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM pg_policies
                            WHERE schemaname = current_schema()
                            AND tablename = '{table}'
                            AND policyname = '{table}_org_policy'
                        ) THEN
                            CREATE POLICY {table}_org_policy ON {table}
                            USING (org_id::text = current_setting('dpp.org_id', true))
                            WITH CHECK (org_id::text = current_setting('dpp.org_id', true));
                        END IF;
                    END
                    $$;
                    """
                )
            )

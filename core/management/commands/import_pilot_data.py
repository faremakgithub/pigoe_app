import re
from decimal import Decimal
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_date, parse_datetime

from core.models import Church, Organization
from events.models import Attendance, Event, EventType
from finance.models import AccountPlan, Contribution, LedgerEntry
from members.models import Member

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Importe les données de la base pilote SQL vers PIGOE. "
        "Commence par les églises puis les membres."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "sql_dump",
            help="Chemin vers le fichier SQL dump de la base pilote.",
        )
        parser.add_argument(
            "--organization-name",
            default="Église des Assemblées de Dieu, Temple de la Grâce de Bassar Kpankissi",
            help="Nom de l'organisation PIGOE à utiliser pour l'import.",
        )

    def handle(self, *args, **options):
        dump_path = Path(options["sql_dump"])
        if not dump_path.exists():
            raise CommandError(f"Fichier SQL introuvable : {dump_path}")

        organization, _ = Organization.objects.get_or_create(
            name=options["organization_name"],
            defaults={"country": "TG", "timezone": "Africa/Lome"},
        )

        import_user = self._get_import_user()

        self.stdout.write(self.style.NOTICE("Import des données pilote commencé."))

        with dump_path.open("r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        with transaction.atomic():
            self._import_churches(content, organization)
            self._import_members(content, organization)
            self._import_account_plans(content, organization)
            self._import_event_types(content, organization)
            self._import_dimes(content, organization, import_user)
            self._import_finances(content, organization, import_user)
            self._import_events(content, organization)
            self._import_event_attendances(content, organization)

        self.stdout.write(self.style.SUCCESS("Import pilote terminé."))

    def _parse_insert_values(self, insert_sql):
        """Extrait une liste de tuples de valeurs depuis un INSERT SQL."""
        values_part = insert_sql.split("VALUES", 1)[1].strip()
        rows = []
        buffer = []
        parens = 0
        token = []
        in_string = False
        escape = False

        for ch in values_part:
            if in_string:
                token.append(ch)
                if escape:
                    escape = False
                    continue
                if ch == "\\":
                    escape = True
                    continue
                if ch == "'":
                    in_string = False
                continue

            if ch == "'":
                in_string = True
                token.append(ch)
                continue

            if ch == "(":
                parens += 1
                token.append(ch)
                continue

            if ch == ")":
                parens -= 1
                token.append(ch)
                if parens == 0:
                    row = ''.join(token).strip()
                    rows.append(row)
                    token = []
                continue

            if parens > 0:
                token.append(ch)

        for row in rows:
            cleaned = row.strip()[1:-1].strip()
            parts = self._split_sql_row(cleaned)
            parsed = [self._parse_sql_value(p) for p in parts]
            yield parsed

    def _split_sql_row(self, row):
        parts = []
        buffer = []
        in_string = False
        escape = False

        for ch in row:
            if in_string:
                buffer.append(ch)
                if escape:
                    escape = False
                    continue
                if ch == "\\":
                    escape = True
                    continue
                if ch == "'":
                    in_string = False
                continue

            if ch == "'":
                in_string = True
                buffer.append(ch)
                continue

            if ch == "," and not in_string:
                parts.append(''.join(buffer).strip())
                buffer = []
                continue

            buffer.append(ch)

        if buffer:
            parts.append(''.join(buffer).strip())

        return parts

    def _parse_sql_value(self, value):
        if value == "NULL":
            return None
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1].replace("''", "'")
        if re.match(r"^-?\d+$", value):
            return int(value)
        if re.match(r"^-?\d+\.\d+$", value):
            return float(value)
        return value

    def _find_insert_matches(self, content, table_name):
        return list(re.finditer(
            rf"INSERT INTO `{table_name}` \(([^)]+)\) VALUES(.+?);\s*(?:--|$)",
            content,
            re.S | re.M,
        ))

    def _iter_insert_rows(self, content, table_name):
        for match in self._find_insert_matches(content, table_name):
            columns = [col.strip(' `') for col in match.group(1).split(",")]
            for values in self._parse_insert_values(match.group(0)):
                yield dict(zip(columns, values))

    def _import_churches(self, content, organization):
        matches = self._find_insert_matches(content, "churches")
        if not matches:
            raise CommandError("INSERT INTO `churches` introuvable dans le dump.")

        for match in matches:
            columns = [col.strip(' `') for col in match.group(1).split(",")]
            for values in self._parse_insert_values(match.group(0)):
                row = dict(zip(columns, values))
            Church.objects.update_or_create(
                legacy_id=row.get("id"),
                defaults={
                    "organization": organization,
                    "hierarchy": row.get("hierarchie") or "",
                    "name": row.get("nom_eglise") or "",
                    "address": row.get("adresse") or "",
                    "location": row.get("localite") or "",
                    "annex_count": row.get("nombre_annexes") or 0,
                    "domain": row.get("domaine_eglise") or "",
                    "member_count": row.get("nombre_fideles") or 0,
                    "founded_at": self._safe_parse_date(row.get("date_creation")),
                    "photo_main": row.get("photo_principale") or "",
                    "photo_secondary": row.get("photo_secondaire") or "",
                    "created_by_id": row.get("created_by"),
                    "created_at": self._parse_datetime_field(row.get("created_at")),
                    "updated_at": self._parse_datetime_field(row.get("updated_at")),
                    "deleted_at": self._parse_datetime_field(row.get("deleted_at")),
                },
            )

        self.stdout.write(self.style.SUCCESS("Import des églises terminé."))

    def _import_members(self, content, organization):
        matches = self._find_insert_matches(content, "members")
        if not matches:
            raise CommandError("INSERT INTO `members` introuvable dans le dump.")

        for match in matches:
            columns = [col.strip(' `') for col in match.group(1).split(",")]
            for values in self._parse_insert_values(match.group(0)):
                row = dict(zip(columns, values))
                church = None
                if row.get("church_id") is not None:
                    church = Church.objects.filter(legacy_id=row.get("church_id")).first()

                Member.objects.update_or_create(
                    legacy_id=row.get("id"),
                    defaults={
                        "organization": organization,
                        "church": church,
                        "membership_number": row.get("matricule") or "",
                        "has_left": bool(row.get("a_quitte")),
                        "is_deceased": bool(row.get("est_decede")),
                        "first_name": row.get("prenom") or "",
                        "last_name": row.get("nom") or "",
                        "phone": self._normalize_phone(row.get("contact_parent"), row.get("id")),
                        "email": row.get("email") or "",
                        "sex": row.get("sexe") or None,
                        "birth_date": self._safe_parse_date(row.get("date_naissance")),
                        "birth_place": row.get("lieu_naissance") or "",
                        "address": row.get("domicile") or "",
                        "profession": row.get("profession") or "",
                        "nationality": row.get("nationalite") or "",
                        "baptism_date": self._safe_parse_date(row.get("date_bapteme")),
                        "baptism_place": row.get("lieu_bapteme") or "",
                        "member_group": row.get("groupe_membre") or "",
                        "conversion_date": self._safe_parse_date(row.get("date_conversion")),
                        "conversion_place": row.get("lieu_conversion") or "",
                        "holy_spirit_date": self._safe_parse_date(row.get("date_saint_esprit")),
                        "holy_spirit_place": row.get("lieu_saint_esprit") or "",
                        "marital_status": self._normalize_marital_status(row.get("situation_matrimoniale") or ""),
                        "children_count": row.get("nombre_enfants"),
                        "spouse": row.get("conjoint") or "",
                        "guardian": row.get("parent_tuteur") or "",
                        "parent_contact": row.get("contact_parent") or "",
                        "activities": row.get("activites") or "",
                        "member_type": row.get("type_membre") or "",
                        "created_at": self._parse_datetime_field(row.get("created_at")),
                        "updated_at": self._parse_datetime_field(row.get("updated_at")),
                        "deleted_at": self._parse_datetime_field(row.get("deleted_at")),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Import des membres terminé."))

    def _parse_datetime_field(self, value):
        return self._safe_parse_datetime(value)

    def _safe_parse_date(self, value):
        """Parse a date string safely, returning None for invalid or zero dates."""
        if not value:
            return None
        # MySQL zero-date values
        if isinstance(value, str) and value.startswith("0000-00-00"):
            return None
        # Strip time portion if present
        if isinstance(value, str) and " " in value:
            value = value.split(" ", 1)[0]
        try:
            return parse_date(value)
        except Exception:
            return None

    def _safe_parse_datetime(self, value):
        """Parse a datetime string safely, returning None for invalid or zero datetimes."""
        if not value:
            return None
        if isinstance(value, str) and value.startswith("0000-00-00"):
            return None
        try:
            dt = parse_datetime(value)
            if dt is not None:
                return dt
            # fallback: try parsing date-only and return midnight
            d = self._safe_parse_date(value)
            if d:
                from datetime import datetime

                return datetime(d.year, d.month, d.day)
            return None
        except Exception:
            return None

    def _normalize_phone(self, phone, row_id):
        if phone and isinstance(phone, str) and phone.startswith("+228") and len(phone) == 12:
            return phone
        return f"+2289900{int(row_id) % 1000000:06d}"

    def _normalize_marital_status(self, raw):
        normalized = raw.strip().lower()
        if "cel" in normalized:
            return "celibataire"
        if "mari" in normalized:
            return "marie"
        if "div" in normalized:
            return "divorce"
        if "veu" in normalized:
            return "veuf"
        return "celibataire"

    def _get_import_user(self):
        user, _ = User.objects.get_or_create(
            username="pilot_importer",
            defaults={
                "email": "pilot_importer@pigoe.local",
                "is_active": False,
            },
        )
        return user

    def _import_dimes(self, content, organization, import_user):
        matches = self._find_insert_matches(content, "dimes")
        if not matches:
            self.stdout.write(self.style.WARNING("INSERT INTO `dimes` introuvable dans le dump."))
            return

        for match in matches:
            columns = [col.strip(' `') for col in match.group(1).split(",")]
            for values in self._parse_insert_values(match.group(0)):
                row = dict(zip(columns, values))
                church = None
                if row.get("church_id") is not None:
                    church = Church.objects.filter(legacy_id=row.get("church_id")).first()

                member = None
                if row.get("member_id") is not None:
                    member = Member.objects.filter(legacy_id=row.get("member_id")).first()

                amount = Decimal(str(row.get("montant"))) if row.get("montant") is not None else Decimal("0")
                if member is None:
                    continue

                payment_method = "cash"
                if row.get("mode_paiement") and "Mobile" in row.get("mode_paiement"):
                    payment_method = "mobile_money"

                Contribution.objects.create(
                    organization=organization,
                    member=member,
                    type=Contribution.Type.DUES,
                    amount=amount,
                    payment_method=payment_method,
                    status=Contribution.Status.CONFIRMED,
                    receipt_number=row.get("numero_recu") or "",
                    cancellation_reason=row.get("observation") or "",
                    created_by=import_user,
                    created_at=self._parse_datetime_field(row.get("created_at")) or None,
                )

        self.stdout.write(self.style.SUCCESS("Import des dîmes terminé."))

    def _import_account_plans(self, content, organization):
        matches = self._find_insert_matches(content, "plancomptables")
        if not matches:
            self.stdout.write(self.style.WARNING("INSERT INTO `plancomptables` introuvable dans le dump."))
            return

        for match in matches:
            columns = [col.strip(' `') for col in match.group(1).split(",")]
            for values in self._parse_insert_values(match.group(0)):
                row = dict(zip(columns, values))
                church = None
                if row.get("church_id") is not None:
                    church = Church.objects.filter(legacy_id=row.get("church_id")).first()

                AccountPlan.objects.update_or_create(
                    legacy_id=row.get("id"),
                    defaults={
                        "organization": organization,
                        "church": church,
                        "title": row.get("intitule") or "",
                        "account_number": row.get("numero_compte") or "",
                        "account_type": row.get("type_compte") or "les_deux",
                        "description": row.get("description") or "",
                        "created_by_id": row.get("created_by"),
                        "created_at": self._parse_datetime_field(row.get("created_at")),
                        "updated_at": self._parse_datetime_field(row.get("updated_at")),
                        "deleted_at": self._parse_datetime_field(row.get("deleted_at")),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Import des plans comptables terminé."))

    def _import_event_types(self, content, organization):
        matches = self._find_insert_matches(content, "typeevents")
        if not matches:
            self.stdout.write(self.style.WARNING("INSERT INTO `typeevents` introuvable dans le dump."))
            return

        for match in matches:
            columns = [col.strip(' `') for col in match.group(1).split(",")]
            for values in self._parse_insert_values(match.group(0)):
                row = dict(zip(columns, values))
                EventType.objects.update_or_create(
                    legacy_id=row.get("id"),
                    defaults={
                        "organization": organization,
                        "name": row.get("libelle") or "",
                        "description": row.get("description") or "",
                        "created_at": self._parse_datetime_field(row.get("created_at")),
                        "updated_at": self._parse_datetime_field(row.get("updated_at")),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Import des types d'événement terminé."))

    def _import_finances(self, content, organization):
        matches = self._find_insert_matches(content, "finances")
        if not matches:
            self.stdout.write(self.style.WARNING("INSERT INTO `finances` introuvable dans le dump."))
            return

        for match in matches:
            columns = [col.strip(' `') for col in match.group(1).split(",")]
            for values in self._parse_insert_values(match.group(0)):
                row = dict(zip(columns, values))
                church = None
                if row.get("church_id") is not None:
                    church = Church.objects.filter(legacy_id=row.get("church_id")).first()

                account_plan = None
                if row.get("plancomptable_id") is not None:
                    account_plan = AccountPlan.objects.filter(legacy_id=row.get("plancomptable_id")).first()

                debit = Decimal(str(row.get("debit"))) if row.get("debit") is not None else Decimal("0")
                credit = Decimal(str(row.get("credit"))) if row.get("credit") is not None else Decimal("0")

                LedgerEntry.objects.update_or_create(
                    legacy_id=row.get("id"),
                    defaults={
                        "organization": organization,
                        "church": church,
                        "account_plan": account_plan,
                        "debit": debit,
                        "credit": credit,
                        "title": row.get("intitule") or "",
                        "operation_date": self._safe_parse_date(row.get("date_operation")),
                        "payment_method": row.get("mode_paiement") or "",
                        "description": row.get("description") or "",
                        "reference_number": row.get("numero_piece") or "",
                        "created_by_id": row.get("created_by"),
                        "created_at": self._parse_datetime_field(row.get("created_at")),
                        "updated_at": self._parse_datetime_field(row.get("updated_at")),
                        "deleted_at": self._parse_datetime_field(row.get("deleted_at")),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Import des écritures financières terminé."))

    def _parse_event_start(self, row):
        if not row.get("date_event"):
            return None
        time_part = row.get("heure_event") or "00:00:00"
        return self._safe_parse_datetime(f"{row.get('date_event')} {time_part}")

    def _import_events(self, content, organization):
        matches = self._find_insert_matches(content, "evenements")
        if not matches:
            self.stdout.write(self.style.WARNING("INSERT INTO `evenements` introuvable dans le dump."))
            return

        for match in matches:
            columns = [col.strip(' `') for col in match.group(1).split(",")]
            for values in self._parse_insert_values(match.group(0)):
                row = dict(zip(columns, values))
                church = None
                if row.get("church_id") is not None:
                    church = Church.objects.filter(legacy_id=row.get("church_id")).first()

                event_type = None
                if row.get("typeevent_id") is not None:
                    event_type = EventType.objects.filter(legacy_id=row.get("typeevent_id")).first()

                Event.objects.update_or_create(
                    legacy_id=row.get("id"),
                    defaults={
                        "organization": organization,
                        "church": church,
                        "event_type": event_type,
                        "title": row.get("specifique_event") or (event_type.name if event_type else ""),
                        "description": row.get("description") or "",
                        "location": row.get("lieu_event") or "",
                        "start_at": self._parse_event_start(row),
                        "created_at": self._parse_datetime_field(row.get("created_at")),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Import des événements terminé."))

    def _import_event_attendances(self, content, organization):
        matches = self._find_insert_matches(content, "evenement_member")
        if not matches:
            self.stdout.write(self.style.WARNING("INSERT INTO `evenement_member` introuvable dans le dump."))
            return

        for match in matches:
            columns = [col.strip(' `') for col in match.group(1).split(",")]
            for values in self._parse_insert_values(match.group(0)):
                row = dict(zip(columns, values))
                event = Event.objects.filter(legacy_id=row.get("evenement_id")).first()
                member = Member.objects.filter(legacy_id=row.get("member_id")).first()
                if not event or not member:
                    continue

                Attendance.objects.update_or_create(
                    event=event,
                    member=member,
                    defaults={
                        "present": True,
                        "role": row.get("role") or "",
                        "note": row.get("note") or "",
                        "checked_in_at": self._parse_datetime_field(row.get("updated_at")) or self._parse_datetime_field(row.get("created_at")),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Import des présences d'événements terminé."))

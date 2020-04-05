"""initial commit

Revision ID: aa9125020ba8
Revises: 
Create Date: 2018-10-24 15:05:36.884559

"""

# revision identifiers, used by Alembic.
revision = "aa9125020ba8"
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question_template", sa.Unicode(length=1024), nullable=True),
        sa.Column("caption", sa.Unicode(length=1024), nullable=True),
        sa.Column("answer_type", sa.Unicode(length=32), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_questions")),
    )
    op.create_table(
        "templates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_templates")),
    )
    op.create_table(
        "users",
        sa.Column("username", sa.Unicode(length=32), nullable=False),
        sa.Column("first_name", sa.Unicode(length=128), nullable=True),
        sa.Column("last_name", sa.Unicode(length=128), nullable=True),
        sa.Column("position", sa.Unicode(length=128), nullable=True),
        sa.Column("manager", sa.Unicode(length=32), nullable=True),
        sa.Column("employee_id", sa.Integer(), nullable=True),
        sa.Column("business_unit", sa.Unicode(length=32), nullable=True),
        sa.Column("location", sa.Unicode(length=64), nullable=True),
        sa.Column("email", sa.Unicode(length=256), nullable=True),
        sa.Column("department", sa.Unicode(length=256), nullable=True),
        sa.Column("has_direct_reports", sa.Boolean(name="b_has_drs"), nullable=True),
        sa.Column("is_staff", sa.Boolean(name="b_is_staff"), nullable=True),
        sa.PrimaryKeyConstraint("username", name=op.f("pk_users")),
    )
    op.create_table(
        "periods",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Unicode(length=16), nullable=True),
        sa.Column("t_id", sa.Integer(), nullable=True),
        sa.Column("enrolment_start_utc", sa.DateTime(), nullable=True),
        sa.Column("entry_start_utc", sa.DateTime(), nullable=True),
        sa.Column("approval_start_utc", sa.DateTime(), nullable=True),
        sa.Column("approval_end_utc", sa.DateTime(), nullable=True),
        sa.Column("ust01_email_last_sent", sa.DateTime(), nullable=True),
        sa.Column("ust02_email_last_sent", sa.DateTime(), nullable=True),
        sa.Column("ust03_email_last_sent", sa.DateTime(), nullable=True),
        sa.Column("ust04_email_last_sent", sa.DateTime(), nullable=True),
        sa.Column("ust05_email_last_sent", sa.DateTime(), nullable=True),
        sa.Column("ust06_email_last_sent", sa.DateTime(), nullable=True),
        sa.Column("ust07_email_last_sent", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "approval_start_utc < approval_end_utc",
            name=op.f("ck_periods_appr_s_lt_appr_e"),
        ),
        sa.CheckConstraint(
            "enrolment_start_utc < entry_start_utc",
            name=op.f("ck_periods_enro_s_lt_entr_s"),
        ),
        sa.CheckConstraint(
            "entry_start_utc < approval_start_utc",
            name=op.f("ck_periods_entr_s_lt_appr_s"),
        ),
        sa.ForeignKeyConstraint(
            ["t_id"], ["templates.id"], name=op.f("fk_periods_t_id_templates")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_periods")),
        sa.UniqueConstraint("name", name=op.f("uq_periods_name")),
    )
    op.create_table(
        "t_rows",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("q_id", sa.Integer(), nullable=True),
        sa.Column("t_id", sa.Integer(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["q_id"], ["questions.id"], name=op.f("fk_t_rows_q_id_questions")
        ),
        sa.ForeignKeyConstraint(
            ["t_id"], ["templates.id"], name=op.f("fk_t_rows_t_id_templates")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_t_rows")),
        sa.UniqueConstraint("t_id", "position", name="uq_template_to_row"),
    )
    op.create_table(
        "requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("to_username", sa.Unicode(length=32), nullable=True),
        sa.Column("from_username", sa.Unicode(length=32), nullable=True),
        sa.Column("period_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["period_id"], ["periods.id"], name=op.f("fk_requests_period_id_periods")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_requests")),
    )
    op.create_table(
        "forms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("to_username", sa.Unicode(length=32), nullable=True),
        sa.Column("from_username", sa.Unicode(length=32), nullable=True),
        sa.Column("period_id", sa.Integer(), nullable=True),
        sa.Column("is_summary", sa.Boolean(name="b_is_summary"), nullable=True),
        sa.Column("is_draft", sa.Boolean(name="b_is_draft"), nullable=True),
        sa.Column("approved_by_username", sa.Unicode(length=32), nullable=True),
        sa.CheckConstraint(
            "from_username != approved_by_username",
            name=op.f("ck_forms_from_neq_approved"),
        ),
        sa.CheckConstraint(
            "from_username != to_username", name=op.f("ck_forms_from_neq_to")
        ),
        sa.CheckConstraint(
            "to_username != approved_by_username", name=op.f("ck_forms_to_neq_approved")
        ),
        sa.ForeignKeyConstraint(
            ["period_id"], ["periods.id"], name=op.f("fk_forms_period_id_periods")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_forms")),
    )
    op.create_table(
        "enrollees",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.Unicode(length=32), nullable=True),
        sa.Column("p_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["p_id"], ["periods.id"], name=op.f("fk_enrollees_p_id_periods")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_enrollees")),
        sa.UniqueConstraint("p_id", "username", name="uq_username_to_p"),
    )
    op.create_table(
        "answers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("form_id", sa.Integer(), nullable=True),
        sa.Column("q_id", sa.Integer(), nullable=True),
        sa.Column("content", sa.Unicode(length=3000), nullable=True),
        sa.ForeignKeyConstraint(
            ["form_id"], ["forms.id"], name=op.f("fk_answers_form_id_forms")
        ),
        sa.ForeignKeyConstraint(
            ["q_id"], ["questions.id"], name=op.f("fk_answers_q_id_questions")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_answers")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("answers")
    op.drop_table("enrollees")
    op.drop_table("forms")
    op.drop_table("requests")
    op.drop_table("t_rows")
    op.drop_table("periods")
    op.drop_table("users")
    op.drop_table("templates")
    op.drop_table("questions")
    # ### end Alembic commands ###

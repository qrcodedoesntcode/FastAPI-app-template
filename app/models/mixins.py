from datetime import datetime

import sqlalchemy as sa


class PrimaryKeyMixin:
    """
    Ajout d'une primary key "id" à toutes les entités
    qui héritent de ce mixin
    Ajoute aussi une méthode "get_by_id" pour récupérer
    l'entité en question à partir de son id
    """

    __abstract__ = True
    id = sa.Column(sa.Integer, primary_key=True)


class TimestampsMixin:
    """
    Définition de deux champs "created_at" et "updated_at".
        - created_at s'initialise une fois à l'insertion, et ne change plus après cela
        - updated_at a la meme valeur que created_at à la création, puis à chaque mise à jour
    de l'entité, le champs se met automatiquement à jour
    """

    __abstract__ = True

    created_at = sa.Column(
        "created_at",
        sa.TIMESTAMP(timezone=False),  # Pas supporté par mysql, mais au cas où
        server_default=sa.text("now()"),
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = sa.Column(
        "updated_at",
        sa.TIMESTAMP(timezone=False),  # Pas supporté par mysql, mais au cas où
        server_default=sa.text("now()"),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

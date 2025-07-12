from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import your models
from models import Base
target_metadata = Base.metadata

# PostgreSQL bağlantı URL'ini doğrudan burada tanımla
DATABASE_URL = "postgresql://yemek_user:yemek123@localhost:5432/yemeksystem"

# alembic.ini'deki URL'i override et
config.set_main_option("sqlalchemy.url", DATABASE_URL)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # PostgreSQL için render_as_batch=False
        render_as_batch=False,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # PostgreSQL için connection ayarları
    configuration = config.get_section(config.config_ini_section, {})
    
    # PostgreSQL bağlantı URL'ini ayarla
    configuration['sqlalchemy.url'] = DATABASE_URL
    
    # PostgreSQL özel ayarları
    configuration['sqlalchemy.pool_pre_ping'] = 'True'
    configuration['sqlalchemy.pool_recycle'] = '300'
    configuration['sqlalchemy.echo'] = 'False'
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.QueuePool,  # PostgreSQL için QueuePool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # PostgreSQL için render_as_batch=False
            render_as_batch=False,
            # PostgreSQL'de compare_type özelliğini aktif et
            compare_type=True,
            # PostgreSQL'de server_default'ları karşılaştır
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
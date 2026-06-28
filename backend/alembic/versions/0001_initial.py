"Initial migration (PostGIS + tables)"
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

revision = '0001'
down_revision = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    op.create_table('projects', sa.Column('id', sa.Integer, primary_key=True), sa.Column('name', sa.String, nullable=False), sa.Column('aoi_geom', Geometry('POLYGON', srid=4326)))
    op.create_table('mineral_occurrences', sa.Column('id', sa.Integer, primary_key=True), sa.Column('name', sa.String), sa.Column('geom', Geometry('POINT', srid=4326)))
    op.create_table('prospectivity_runs', sa.Column('id', sa.Integer, primary_key=True))
    op.create_index('idx_aoi', 'projects', ['aoi_geom'], postgresql_using='gist')

def downgrade():
    pass
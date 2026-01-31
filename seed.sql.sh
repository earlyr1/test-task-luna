#!/usr/bin/env bash
set -e

# -------------------------
# psql-like args
# -------------------------
PSQL_ARGS=()
export PGPASSWORD=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|-U|-d|-p)
      PSQL_ARGS+=("$1" "$2")
      shift 2
      ;;
    --password)
      export PGPASSWORD="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [ -z "$PGPASSWORD" ]; then
  echo "❌ --password is required"
  exit 1
fi

psql "${PSQL_ARGS[@]}" << 'SQL'
BEGIN;

-- =========================
-- CLEAN
-- =========================
TRUNCATE
  org_x_activities,
  organizations,
  activity,
  buildings
RESTART IDENTITY CASCADE;

-- =========================
-- BUILDINGS (30)
-- coords: int 1..100
-- =========================
INSERT INTO buildings (address, location)
SELECT
  'Test street ' || i,
  ST_SetSRID(ST_MakePoint(
    (random()*99 + 1)::int,
    (random()*99 + 1)::int
  ), 4326)::geography
FROM generate_series(1, 30) AS i;

-- =========================
-- ACTIVITIES TREE
-- lvl0 -> lvl1 -> lvl2 -> lvl3
-- =========================

-- lvl0 (5)
INSERT INTO activity (name, parent_activity_id)
SELECT
  'lvl0_' || i,
  NULL
FROM generate_series(1, 5) i;

-- lvl1 (по 2 на каждый lvl0)
INSERT INTO activity (name, parent_activity_id)
SELECT
  'lvl1_' || i,
  a.id
FROM activity a
CROSS JOIN generate_series(1, 2) i
WHERE a.parent_activity_id IS NULL;

-- lvl2 (по 2)
INSERT INTO activity (name, parent_activity_id)
SELECT
  'lvl2_' || i,
  a.id
FROM activity a
CROSS JOIN generate_series(1, 2) i
WHERE a.name LIKE 'lvl1_%';

-- lvl3
INSERT INTO activity (name, parent_activity_id)
SELECT
  'lvl3',
  a.id
FROM activity a
WHERE a.name LIKE 'lvl2_%'
  AND random() < 0.6;

-- =========================
-- ORGANIZATIONS (100)
-- несколько в одном здании
-- =========================
INSERT INTO organizations (name, phone_numbers, building_id)
SELECT
  'Organization_' || i,
  ARRAY['+100000' || lpad(i::text, 3, '0')],
  greatest(1, (random() * 30) ::int)
FROM generate_series(1, 100) i;


-- =========================
-- ORG ↔ ACTIVITY
-- фирмы сидят и в листьях и в середине
-- =========================
INSERT INTO org_x_activities (org_id, activity_id)
SELECT DISTINCT
  o.id,
  a.id
FROM organizations o
CROSS JOIN LATERAL (
  SELECT id
  FROM activity
  WHERE random() < 0.4
) a WHERE random() < 0.1;

\echo ''
\echo '========== BUILDINGS → ORGANIZATIONS[ACTIVITIES] (GROUP BY) =========='
\echo ''

SELECT
  b.id                                    AS building_id,
  ST_X(b.location::geometry)::int         AS x,
  ST_Y(b.location::geometry)::int         AS y,
  string_agg(
    format('%s %s [%s]', 
      o.id, 
      o.name,
      COALESCE(act.activities, 'no activities')
    ),
    E'\n\t' ORDER BY o.id
  ) AS organizations
FROM buildings b
JOIN organizations o ON o.building_id = b.id
LEFT JOIN (
  SELECT 
    org_id,
    string_agg(activity_id::text, ', ' ORDER BY activity_id) AS activities
  FROM org_x_activities
  GROUP BY org_id
) act ON act.org_id = o.id
GROUP BY b.id, b.location
ORDER BY b.id;

\echo ''
\echo '========================='
\echo 'Activities tree'
\echo '========================='
\echo ''


WITH RECURSIVE activity_tree AS (
  -- Корневые элементы
  SELECT 
    id,
    name,
    parent_activity_id,
    id::text AS path,
    0 AS level
  FROM activity
  WHERE parent_activity_id IS NULL
  
  UNION ALL
  
  -- Потомки
  SELECT 
    a.id,
    a.name,
    a.parent_activity_id,
    at.path || ' -> ' || a.id::text,
    at.level + 1
  FROM activity a
  JOIN activity_tree at ON a.parent_activity_id = at.id
)
SELECT 
  REPEAT('  ', level) || '└─ ' || name || ' ' || 'id' || id AS tree,
  level,
  path
FROM activity_tree
ORDER BY path;

COMMIT;
SQL

echo "✅ DB seeded"

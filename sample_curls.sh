# 1. Получить организации по building_id (замени 1 на реальный ID)
curl -X GET "http://localhost:8000/orgs/buildings/1" \
  -H "X-API-Key: ffhv8983fby763_^ddvs66ech"

# 2. Получить организации по activity_id (замени 1 на реальный ID)
curl -X GET "http://localhost:8000/orgs/activities/1" \
  -H "X-API-Key: ffhv8983fby763_^ddvs66ech"

# 3. Получить организацию по ID (замени 1 на реальный ID)
curl -X GET "http://localhost:8000/orgs/1" \
  -H "X-API-Key: ffhv8983fby763_^ddvs66ech"

# 4. Поиск организаций по имени
curl -X GET "http://localhost:8000/orgs/search/by-name?name=Test" \
  -H "X-API-Key: ffhv8983fby763_^ddvs66ech"

# 5. Поиск организаций в радиусе
curl -X GET "http://localhost:8000/orgs/search/radius?lat=55.75&lon=37.62&radius=500" \
  -H "X-API-Key: ffhv8983fby763_^ddvs66ech"

# 6. Поиск организаций в прямоугольнике
curl -X GET "http://localhost:8000/orgs/search/rectangle?lat_min=55.70&lon_min=37.60&lat_max=55.80&lon_max=37.70" \
  -H "X-API-Key: ffhv8983fby763_^ddvs66ech"

# 7. Поиск организаций по дереву активностей (замени 1 на реальный ID)
curl -X GET "http://localhost:8000/orgs/search/activity/1" \
  -H "X-API-Key: ffhv8983fby763_^ddvs66ech"
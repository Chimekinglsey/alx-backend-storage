-- 2. Best band ever!
-- A script to rank country origins of bands
SELECT TRIM(origin) AS origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY TRIM(origin)
ORDER BY nb_fans
DESC;
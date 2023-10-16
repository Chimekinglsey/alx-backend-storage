-- 2. Best band ever!
-- A script to rank country origins of bands
SELECT origin, fans AS nb_fans
FROM metal_bands
ORDER BY fans
DESC;
-- 3. Old school band
-- A script that lists all bands with`Glam rock` as their main style, ranked by longevity
select trim(band_name) as band_name, (IF split != NULL THEN SET lifespan = YEAR(formed) - YEAR(DATE_SUB(CURDATE(), INTERVAL 1 YEAR)) ELSE THEN SET lifespan = YEAR(formed) - YEAR(split)) as lifespan

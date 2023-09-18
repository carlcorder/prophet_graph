SELECT
                bd.name             as "lib_name",
                p1.name             as "prod_name",
                p2.name             as "same_as_prod",                                -- Master Product
                bd.businessdbid     as "lib_id",
                p1.productid        as "prod_id"
FROM
                product          p1
    left  join  product          p2 on p2.productid    = p1.linkedproductid
    inner join  businessdatabase bd on bd.businessdbid = p1.businessdbid
ORDER BY
                                       "lib_name",
                                       "prod_name",
                                       "same_as_prod"
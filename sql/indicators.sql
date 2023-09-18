SELECT
    bd.name                         as  "lib_name",
    p.name                          as  "prod_name",
    i.name                          as  "ind_name",
    i.indicatortype                 as  "ind_type_flag",                              -- Simple Indicator (No Selection Criteria) = 0
    bd.businessdbid                 as  "lib_id",
    p.productid                     as  "prod_id",
    i.indicatorid                   as  "ind_id"
FROM
               indicator        i
    left  join prodindlink      pil on  pil.indicatorid   = i.indicatorid
    left  join product          p   on  p.productid       = pil.productid
                                    and p.linkedproductid = 0
    inner join businessdatabase bd  on  bd.businessdbid   = p.businessdbid
UNION
SELECT
    bd.name                         as  "lib_name",
    null                            as  "prod_name",
    i.name                          as  "ind_name",
    i.indicatortype                 as  "ind_type",
    bd.businessdbid                 as  "lib_id",
    null                            as  "prod_id",
    i.indicatorid                   as  "ind_id"
FROM
               indicator        i
    inner join businessdatabase bd  on  bd.businessdbid   = i.businessdbid
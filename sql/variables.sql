SELECT
               v.name                 as  "var_name",
               vi.vartype             as  "input_var_flag",                           -- Core, Primary Input, Secondary Input (Blank Ind Expression)
               vd.librarydefflag      as  "alt_defn_flag",                            -- Core, Default, Alternative
               bd.name                as  "lib_name",                                 -- AND NOT DEFAULT_*
               p.name                 as  "prod_name",
               vd.indicatorexpr       as  "ind_expr",
               vd.ordernumber         as  "defn_num",                                 -- 0+
               vd.vartype             as  "defn_type",                                -- Formula, Constant, Global, Parameter, Model Point, etc.
               vd.variableexpr        as  "var_expr",
               bd.businessdbid        as  "lib_id",
               vd.productid           as  "prod_id",
               vd.variabledefnid      as  "var_id"
FROM
               variabledefn      vd
    inner join variableinfo      vi   on  vi.variableinfoid = vd.variableinfoid
                                      and vd.librarydefflag = 0                       -- Ignore Alternative Definitions
    inner join businessdatabase  bd   on  bd.businessdbid   = vi.businessdbid
    inner join variables         v    on  v.variableid      = vi.variableid
    left  join product           p    on  p.productid       = vd.productid
ORDER BY
                                          "var_name",
                                          "lib_name",
                                          "prod_name",
                                          "defn_num"
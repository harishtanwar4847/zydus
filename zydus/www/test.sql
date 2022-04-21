select * from(select "Project" as doctype, P.route,P._liked_by as liked_by,B.color,P.name,B.brand_logo,P.title,count(V.reference_name) as view,concat(P.month," ",P.year) as month_year from `tabProject` as P  left join `tabBrand` as B on P.brand = B.name left join `tabView Log` as V on V.reference_name= name and V.reference_doctype= doctype group by P.name having count(V.reference_name) > 0 order by count(V.reference_name) desc)z 
union all 
select * from(select "Datasheet" as doctype, D.data_type, D._liked_by as liked_by,B.color,D.name,B.brand_logo,D.title,count(V.reference_name) as view,concat(D.month," ",D.year) as month_year from `tabDatasheet` as D  left join `tabBrand` as B on D.brand = B.name left join `tabView Log` as V on V.reference_name= name and V.reference_doctype= doctype group by D.name having count(V.reference_name) > 0  order by count(V.reference_name) desc)z limit 6



select T.doctype,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,B.brand_logo,count(V.reference_name) as view_count from 
(select "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.title,concat(P.month," ",P.year) as month_year from `tabProject` as P 
union
select "Datasheet" as doctype, D.data_type, D._liked_by as liked_by,D.brand,D.name,D.title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D) as T left join `tabBrand` as B on T.brand = B.name left join `tabView Log` as V on V.reference_name= T.name and V.reference_doctype= T.doctype group by T.name having view_count > 0 order by view_count desc;


select T.doctype,T.route,T.liked_by,T.name,T.title,T.month_year,B.color,B.brand_name from 
(select "Project" as doctype, P.route,P._liked_by as liked_by,P.brand,P.name,P.title,concat(P.month," ",P.year) as month_year from `tabProject` as P 
union
select "Datasheet" as doctype, D.data_type, D._liked_by as liked_by,D.brand,D.name,D.title,concat(D.month," ",D.year) as month_year from `tabDatasheet`as D) as T left join `tabBrand` as B on T.brand = B.name group by T.name

 




match (p:Provider)-[r]->(b:Bidding)<-[]-(u:User)
with p, (sum(toInteger(r.monto_unitario)) * sum(toInteger(r.cantidad))) as money, count(b) as cb, u order by cb desc limit 1
match path = (provider:Provider)-[*2]-(:User)
where provider = p
return path

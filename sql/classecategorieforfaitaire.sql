delete from classecategorieforfaitaire;
alter table classecategorieforfaitaire drop column debut, drop column fin, drop column deb_ifpb, drop column fin_ifpb;
alter table classecategorieforfaitaire add column debut integer, add column fin integer, add column deb_ifpb integer, add column fin_ifpb integer;
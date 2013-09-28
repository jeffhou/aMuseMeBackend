drop table if exists popularities;
create table popularities (
  id integer primary key autoincrement,
  atom_id text not null,
  genre integer not null,
  rank integer not null
);

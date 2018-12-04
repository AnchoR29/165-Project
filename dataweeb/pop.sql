delete FROM Anime;
delete FROM Manga;
delete from Author;
delete FROM Episodes;
delete FROM Studio;
delete FROM Genre;


insert into Anime values ('1','Title 1','12-12-1222','TV','12','Studio 1','Action');
insert into Anime values ('2','Title 2 ','12-12-1222','TV','12','Studio 2','Action');
insert into Anime values ('3','Title 3','12-12-1222','TV','12','Studio 3','Action');
insert into Anime values ('4','Title 4','12-12-1222','TV','12','Studio 4','Action');

insert into Manga values ('1','Title 1','12-12-1222','Ongoing','12','Author 1','Action');
insert into Manga values ('2','Title 2 ','12-12-1222','Finished','12','Author 2','Action');
insert into Manga values ('3','Title 3','12-12-1222','Ongoing','12','Author 3','Action');
insert into Manga values ('4','Title 4','12-12-1222','Finished','12','Author 4','Action');

insert into Author values ('1','Author 1');
insert into Author values ('2','Author 2 ');
insert into Author values ('3','Author 3');
insert into Author values ('4','Author 4');

insert into Episodes values ('1','1','Title 1','12-12-1222','1');
insert into Episodes values ('2','1','Title 1 ','12-12-1222','2');
insert into Episodes values ('3','2','Title 2','12-12-1222','1');
insert into Episodes values ('4','2','Title 2','12-12-1222','2');

insert into Studio values ('1','Studio 1');
insert into Studio values ('2','Studio 2');
insert into Studio values ('3','Studio 3');
insert into Studio values ('4','Studio 4');

insert into Genre values ('1','Genre 1','Description 1');
insert into Genre values ('2','Genre 2 ','Description 2');
insert into Genre values ('3','Genre 3','Description 3');
insert into Genre values ('4','Genre 4','Description 4');
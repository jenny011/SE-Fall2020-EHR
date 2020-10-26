#inserts
insert into hospital values ('1', 'A', '111', '1st st.', NULL);

insert into department values ('1', '1', 'ER', '222', 'Room ER', NULL);

insert into doctor values ('1', '1', '1', SHA2('123', 256), 'Alice', 'alice@email.com', '123', 'Room 101');

insert into nurse values ('1', '1', '1', SHA2('123', 256), 'Bob', 'bob@email.com', '456', 'Room 102');

insert into patient values ('1', SHA2('123', 256), 'Cat', 'cat@email.com', '789', '1st ave.', 20, 'female', 'A', NULL);
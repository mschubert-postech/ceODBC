/*-----------------------------------------------------------------------------
 * SetupTest.sql
 *   Creates the objects used for testing ceODBC with a PostgreSQL database.
 *---------------------------------------------------------------------------*/

create table TestDates (
    IntCol                              integer not null,
    DateCol                             date not null,
    TimestampCol                        timestamp not null,
    TimestampTZCol                      timestamptz not null,
    NullableDateCol                     date,
    NullableTimestampCol                timestamp,
    NullableTimestampTZCol              timestamptz
);

create table TestNumbers (
    IntCol              integer not null,
    BigIntCol           bigint,
    DecimalCol          decimal(6, 2)
);

create table TestStrings (
    IntCol              integer not null,
    StringCol           varchar(20) not null,
    NullableCol         varchar(50)
);

create table TestTempTable (
    IntCol              integer not null,
    StringCol           varchar(255)
);

alter table TestTempTable add constraint TestTempTable_pk
primary key (IntCol);

create function sp_Test (
    a_InValue varchar(50),
    inout a_InOutValue bigint,
    out a_OutValue decimal(6, 2)
) returns record as $$
begin
    a_InOutValue := a_InOutValue * 2;
    a_OutValue := length(a_InValue) * 1.25;
end;
$$ LANGUAGE plpgsql;

create function sp_TestNoArgs()
returns void as $$
begin
    null;
end;
$$ LANGUAGE plpgsql;

delete from TestNumbers;

insert into TestNumbers
values (1, 25, 125.25);

insert into TestNumbers
values (2, 1234567890123456, 245.37);

insert into TestNumbers
values (3, 9876543210, 25.99);

insert into TestNumbers
values (4, 98765432101234, 445.79);

delete from TestStrings;

insert into TestStrings
values (1, 'String 1', null);

insert into TestStrings
values (2, 'String 2B', 'Nullable One');

insert into TestStrings
values (3, 'String 3XX', null);

insert into TestStrings
values (4, 'String 4YYY', 'Nullable Two');

insert into TestDates
values (1, '2020-02-08', '2019-12-20 18:35:25', '2018-11-18 23:59:59',
           '1969-07-29', '1988-01-25 08:24:13', '1999-12-31 17:00:05');

insert into TestDates
values (2, '1978-02-12', '2009-02-20 08:23:12', '2016-09-15 11:47:46',
           null, null, null);

insert into TestDates
values (3, '2000-06-18', '2007-01-28 06:22:11', '2008-05-27 01:25:11',
           '1988-06-30', '1998-04-29 11:35:24', '2005-08-15 22:00:00');

insert into TestDates
values (4, '1999-10-05', '2009-02-19 00:01:02', '2020-11-28 10:51:23',
           null, null, null);

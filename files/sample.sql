CREATE TABLE departments (
  id   integer PRIMARY KEY,
  name text NOT NULL
);

CREATE TABLE employees (
  id            integer PRIMARY KEY,
  name          text NOT NULL,
  department_id integer REFERENCES departments(id),
  salary        integer NOT NULL,
  hired_on      date NOT NULL
);

INSERT INTO departments (id, name) VALUES
  (1, '総務部'),
  (2, '営業部'),
  (3, '開発部');

INSERT INTO employees (id, name, department_id, salary, hired_on) VALUES
  (1, '佐藤', 1, 280000, '2018-04-01'),
  (2, '鈴木', 2, 320000, '2015-04-01'),
  (3, '高橋', 3, 350000, '2016-10-01'),
  (4, '田中', 2, 250000, '2022-04-01'),
  (5, '伊藤', 3, 300000, '2020-04-01'),
  (6, '渡辺', NULL, 230000, '2024-04-01');

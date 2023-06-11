-- Create the users table
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username TEXT,
  event_id INTEGER
);

-- Create the progress table
CREATE TABLE IF NOT EXISTS progress (
  id INTEGER PRIMARY KEY,
  player_id INTEGER,
  objective_id INTEGER,
  FOREIGN KEY (player_id) REFERENCES users (id)
);

-- Create the players table
CREATE TABLE IF NOT EXISTS players (
  id INTEGER PRIMARY KEY,
  coin_balance INTEGER,
  experience INTEGER,
  level INTEGER,
  last_login DATETIME
  -- Add more columns as needed
);

-- Insert sample data into the users table
INSERT INTO users (username, event_id) VALUES
  ('JohnDoe', 1),
  ('JaneSmith', 2),
  ('BobJohnson', 1);

-- Insert sample data into the progress table
INSERT INTO progress (player_id, objective_id) VALUES
  (1, 1),
  (1, 2),
  (2, 1),
  (3, 2);

-- Insert sample data into the players table
INSERT INTO players (id, coin_balance, experience, level, last_login) VALUES
  (1, 100, 500, 5, '2023-06-01 10:00:00'),
  (2, 50, 250, 3, '2023-06-02 15:30:00'),
  (3, 200, 1000, 8, '2023-06-03 08:45:00');

-- Add more sample data for other tables if needed

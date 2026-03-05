-- 010_schema.sql
USE mlb_passport;

-- USERS
CREATE TABLE IF NOT EXISTS users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GAMES (minimal fields; we’ll add more later)
CREATE TABLE IF NOT EXISTS games (
  game_id INT AUTO_INCREMENT PRIMARY KEY,
  mlb_game_pk INT NOT NULL UNIQUE,
  game_date DATE NOT NULL,
  home_team VARCHAR(10) NOT NULL,
  away_team VARCHAR(10) NOT NULL,
  venue_name VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ATTENDANCE (many-to-many)
CREATE TABLE IF NOT EXISTS user_games (
  user_id INT NOT NULL,
  game_id INT NOT NULL,
  attended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes VARCHAR(500),
  PRIMARY KEY (user_id, game_id),
  CONSTRAINT fk_user_games_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_user_games_game FOREIGN KEY (game_id) REFERENCES games(game_id) ON DELETE CASCADE
);
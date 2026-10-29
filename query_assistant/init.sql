
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    online_order TEXT,
    book_table TEXT,
    rate TEXT,
    votes INTEGER,
    approx_cost INTEGER,
    listed_in_type TEXT
);


CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_restaurants_type ON restaurants(listed_in_type);
CREATE INDEX idx_restaurants_cost ON restaurants(approx_cost);
CREATE INDEX idx_sessions_time ON sessions(created_at);


INSERT INTO restaurants (name, online_order, book_table, rate, votes, approx_cost, listed_in_type) VALUES 
('Sample Restaurant', 'Yes', 'No', '4.0/5', 100, 500, 'Dining');

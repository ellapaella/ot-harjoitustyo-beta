
CREATE TABLE Users (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP DEFAULT NOW(), 
    username TEXT UNIQUE, 
    passhash TEXT, 
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE Plots (
    id SERIAL PRIMARY KEY, 
    created TIMESTAMP DEFAULT NOW(), 
    owner_id INTEGER REFERENCES Users, 
    plot_name TEXT, 
    description TEXT
);
